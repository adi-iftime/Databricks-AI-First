"""Generate deterministic sample sales CSV data."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timedelta
from pathlib import Path
from random import Random


HEADERS = ["id", "product", "quantity", "price", "timestamp"]
PRODUCTS = [
    ("Keyboard", 49.99),
    ("Mouse", 19.99),
    ("Monitor", 229.99),
    ("Laptop Stand", 34.50),
    ("USB-C Cable", 9.99),
    ("Webcam", 89.00),
    ("Headset", 59.99),
    ("Docking Station", 149.00),
    ("Microphone", 129.99),
]


def generate_rows(size: int, seed: int) -> list[list[str]]:
    rng = Random(seed)
    start = datetime(2026, 4, 1, 9, 0, 0)
    rows: list[list[str]] = []

    for offset in range(size):
        record_id = str(1001 + offset)
        product, base_price = PRODUCTS[rng.randrange(len(PRODUCTS))]
        quantity = rng.randint(1, 5)
        price = round(base_price + rng.uniform(-2.0, 2.0), 2)
        ts = start + timedelta(minutes=offset * 37)
        rows.append([record_id, product, str(quantity), f"{price:.2f}", ts.isoformat()])

    # Add edge cases to exercise Silver cleansing and expectations.
    rows.extend(
        [
            ["1002", "Mouse", "2", "19.99", "2026-04-02T12:45:00"],  # duplicate id
            ["1900", "", "1", "39.99", "2026-04-03T15:45:00"],  # missing product
            ["1901", "Desk Lamp", "", "25.00", "2026-04-04T12:00:00"],  # null quantity
            ["1902", "Invalid Price", "1", "-5.00", "2026-04-04T13:00:00"],  # bad price
            ["1903", "Missing TS", "1", "30.00", ""],  # null timestamp
        ]
    )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate sample CSV for DLT demo.")
    parser.add_argument("--rows", type=int, default=10, help="Number of clean base rows.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed for determinism.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/sample.csv"),
        help="Output CSV path.",
    )
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    rows = generate_rows(size=args.rows, seed=args.seed)
    with args.output.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(HEADERS)
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()

