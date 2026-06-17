#!/usr/bin/env python3
"""Validate generated adversarial safety prompt JSONL files."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_FIELDS = {
    "id",
    "category",
    "difficulty",
    "risk_type",
    "prompt",
    "expected_behavior",
    "source",
}

ALLOWED_DIFFICULTIES = {"easy", "medium", "hard"}


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"Line {line_no} is not a JSON object")
            rows.append(row)
    return rows


def load_allowed_categories(path: Path) -> set[str]:
    categories: set[str] = set()
    if not path.exists():
        return categories
    for row in load_jsonl(path):
        category = row.get("category")
        if isinstance(category, str) and category:
            categories.add(category)
    return categories


def validate_rows(rows: List[Dict[str, Any]], allowed_categories: set[str]) -> List[str]:
    errors: List[str] = []
    seen_ids: set[str] = set()

    for idx, row in enumerate(rows, start=1):
        missing = REQUIRED_FIELDS - set(row.keys())
        if missing:
            errors.append(f"line {idx}: missing fields: {sorted(missing)}")

        row_id = row.get("id")
        if not isinstance(row_id, str) or not row_id.strip():
            errors.append(f"line {idx}: id must be a non-empty string")
        elif row_id in seen_ids:
            errors.append(f"line {idx}: duplicate id: {row_id}")
        else:
            seen_ids.add(row_id)

        category = row.get("category")
        if not isinstance(category, str) or not category.strip():
            errors.append(f"line {idx}: category must be a non-empty string")
        elif allowed_categories and category not in allowed_categories:
            errors.append(f"line {idx}: unknown category: {category}")

        difficulty = row.get("difficulty")
        if difficulty not in ALLOWED_DIFFICULTIES:
            errors.append(f"line {idx}: difficulty must be one of {sorted(ALLOWED_DIFFICULTIES)}")

        for field in ["prompt", "expected_behavior", "risk_type", "source"]:
            value = row.get(field)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"line {idx}: {field} must be a non-empty string")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate generated JSONL dataset.")
    parser.add_argument("--input", required=True, help="Path to generated JSONL file.")
    parser.add_argument("--seed-categories", default="data/seed_categories.jsonl", help="Path to seed category JSONL.")
    args = parser.parse_args()

    input_path = Path(args.input)
    rows = load_jsonl(input_path)
    allowed_categories = load_allowed_categories(Path(args.seed_categories))
    errors = validate_rows(rows, allowed_categories)

    if errors:
        print(f"Validation failed for {input_path}: {len(errors)} error(s)")
        for error in errors[:50]:
            print(f"- {error}")
        if len(errors) > 50:
            print(f"... and {len(errors) - 50} more")
        raise SystemExit(1)

    print(f"Validation passed for {input_path}: {len(rows)} rows, 0 errors")


if __name__ == "__main__":
    main()
