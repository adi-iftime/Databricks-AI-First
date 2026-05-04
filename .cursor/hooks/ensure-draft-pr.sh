#!/usr/bin/env bash
# Ensures a single DRAFT GitHub PR for the current branch after a successful push.
# Implements the automation side of .cursor/agents/pr-writer-agent.md (draft default, no duplicates).
set -euo pipefail

INPUT_JSON=$(cat)

if ! command -v jq >/dev/null 2>&1; then
  echo '{}' >&2
  exit 0
fi

command_for() {
  echo "$INPUT_JSON" | jq -r '.tool_input.command // .command // empty'
}

is_git_push() {
  local cmd="$1"
  [[ "$cmd" =~ git[[:space:]]+push ]] || [[ "$cmd" =~ &&[[:space:]]+git[[:space:]]+push ]]
}

is_dry_run_push() {
  local cmd="$1"
  [[ "$cmd" == *"--dry-run"* ]]
}

push_succeeded_post_tool() {
  local raw
  raw=$(echo "$INPUT_JSON" | jq -r '.tool_output // empty')
  [[ -z "$raw" ]] && return 1
  local code
  code=$(echo "$raw" | jq -r '.exitCode // empty' 2>/dev/null || true)
  [[ "$code" == "0" ]]
}

push_succeeded_after_shell() {
  local out
  out=$(echo "$INPUT_JSON" | jq -r '.output // empty')
  # Heuristic: failed pushes usually mention rejection or fatal
  if echo "$out" | grep -qiE '(fatal:|error: failed to push|rejected|Permission denied)'; then
    return 1
  fi
  return 0
}

resolve_workdir() {
  local wd
  wd=$(echo "$INPUT_JSON" | jq -r '.cwd // .tool_input.working_directory // empty')
  if [[ -n "$wd" && -d "$wd" ]]; then
    echo "$wd"
    return 0
  fi
  if git rev-parse --show-toplevel >/dev/null 2>&1; then
    git rev-parse --show-toplevel
    return 0
  fi
  echo ""
}

detect_base_branch() {
  local repo="$1"
  git -C "$repo" rev-parse --verify origin/main >/dev/null 2>&1 && echo main && return 0
  git -C "$repo" rev-parse --verify origin/master >/dev/null 2>&1 && echo master && return 0
  echo main
}

normalize_feature_key() {
  local b="$1"
  b="${b#cursor/}"
  b="${b#feature/}"
  b="${b#fix/}"
  b="${b#refactor/}"
  b="${b#chore/}"
  echo "$b"
}

main() {
  local cmd
  cmd=$(command_for)
  if ! is_git_push "$cmd" || is_dry_run_push "$cmd"; then
    echo '{}'
    exit 0
  fi

  # postToolUse: require success exit code; afterShellExecution: heuristic only
  if echo "$INPUT_JSON" | jq -e '.tool_output' >/dev/null 2>&1; then
    push_succeeded_post_tool || { echo '{}'; exit 0; }
  else
    push_succeeded_after_shell || { echo '{}'; exit 0; }
  fi

  if ! command -v gh >/dev/null 2>&1 || ! command -v git >/dev/null 2>&1; then
    echo '{}' >&2
    exit 0
  fi

  local workdir
  workdir=$(resolve_workdir)
  if [[ -z "$workdir" ]]; then
    echo '{}'
    exit 0
  fi

  if ! git -C "$workdir" rev-parse --git-dir >/dev/null 2>&1; then
    echo '{}'
    exit 0
  fi

  if ! (cd "$workdir" && gh auth status) >/dev/null 2>&1; then
    echo '{}' >&2
    exit 0
  fi

  local branch base
  branch=$(git -C "$workdir" branch --show-current 2>/dev/null || true)
  if [[ -z "$branch" ]]; then
    echo '{}'
    exit 0
  fi

  base=$(detect_base_branch "$workdir")
  local fkey
  fkey=$(normalize_feature_key "$branch")

  git -C "$workdir" fetch origin "$base" 2>/dev/null || true

  local title stat files body_tmp pr_url
  title=$(git -C "$workdir" log -1 --format='%s')
  stat=$(git -C "$workdir" diff --stat "origin/${base}...HEAD" 2>/dev/null || git -C "$workdir" diff --stat "${base}...HEAD" 2>/dev/null || echo "(no diff stat)")
  files=$(git -C "$workdir" diff --name-only "origin/${base}...HEAD" 2>/dev/null || git -C "$workdir" diff --name-only "${base}...HEAD" 2>/dev/null || true)

  body_tmp=$(mktemp)
  trap 'rm -f "$body_tmp"' EXIT

  {
    echo "**Feature:** \`${fkey}\`"
    echo ""
    echo "## Context"
    echo "Automated draft PR after \`git push\` (repo hook: \`.cursor/hooks/ensure-draft-pr.sh\`). Aligned with \`.cursor/agents/pr-writer-agent.md\` (draft default, one PR per branch)."
    echo ""
    echo "## Changes"
    echo '```'
    echo "$stat"
    echo '```'
    echo ""
    echo "### Files"
    if [[ -n "$files" ]]; then
      echo "$files" | sed 's/^/- /'
    else
      echo "- _(no file list)_"
    fi
    echo ""
    echo "## How to test"
    echo "- Review diff against \`${base}\`"
    echo "- Run project tests / CI as usual"
    echo ""
    echo "## Notes"
    echo "- **Draft** — mark ready for review only when explicitly requested."
  } >"$body_tmp"

  local existing
  existing=$(cd "$workdir" && gh pr list --head "$branch" --json number --jq '.[0].number' 2>/dev/null || true)

  if [[ -n "$existing" && "$existing" != "null" ]]; then
    (cd "$workdir" && gh pr edit "$existing" --body-file "$body_tmp") >/dev/null
    pr_url=$(cd "$workdir" && gh pr view "$existing" --json url --jq '.url' 2>/dev/null || echo "")
  else
    if ! (cd "$workdir" && gh pr create --draft --base "$base" --head "$branch" --title "$title" --body-file "$body_tmp") >/dev/null 2>&1; then
      # Race or already exists: re-check
      existing=$(cd "$workdir" && gh pr list --head "$branch" --json number --jq '.[0].number' 2>/dev/null || true)
      if [[ -n "$existing" && "$existing" != "null" ]]; then
        (cd "$workdir" && gh pr edit "$existing" --body-file "$body_tmp") >/dev/null
        pr_url=$(cd "$workdir" && gh pr view "$existing" --json url --jq '.url' 2>/dev/null || echo "")
      else
        echo '{}'
        exit 0
      fi
    else
      pr_url=$(cd "$workdir" && gh pr list --head "$branch" --json url --jq '.[0].url' 2>/dev/null || echo "")
    fi
  fi

  if [[ -n "$pr_url" ]]; then
    # Only inject chat context for postToolUse (Shell tool); afterShellExecution would duplicate if we always emitted.
    if echo "$INPUT_JSON" | jq -e '.tool_output' >/dev/null 2>&1; then
      local msg
      msg="Auto (hooks): draft PR for branch \`${branch}\`: ${pr_url}. Body matches latest push vs \`${base}\`. Policy: \`.cursor/agents/pr-writer-agent.md\` (draft default; one PR per branch)."
      jq -n --arg ctx "$msg" '{additional_context: $ctx}'
    else
      echo '{}'
    fi
  else
    echo '{}'
  fi
  exit 0
}

main "$@"
