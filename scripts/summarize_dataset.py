#!/usr/bin/env python3
"""Create a Markdown summary for a generated adversarial prompt dataset."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_no}: {exc}") from exc
    return rows


def make_report(rows: List[Dict[str, Any]], input_path: Path) -> str:
    category_counts = Counter(row.get("category", "unknown") for row in rows)
    difficulty_counts = Counter(row.get("difficulty", "unknown") for row in rows)
    risk_counts = Counter(row.get("risk_type", "unknown") for row in rows)

    lines: List[str] = []
    lines.append("# Generation Report")
    lines.append("")
    lines.append(f"Input file: `{input_path}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total rows: {len(rows)}")
    lines.append(f"- Unique categories: {len(category_counts)}")
    lines.append(f"- Unique risk types: {len(risk_counts)}")
    lines.append("")

    lines.append("## Counts by category")
    lines.append("")
    for category, count in category_counts.most_common():
        lines.append(f"- {category}: {count}")
    lines.append("")

    lines.append("## Counts by difficulty")
    lines.append("")
    for difficulty, count in difficulty_counts.most_common():
        lines.append(f"- {difficulty}: {count}")
    lines.append("")

    lines.append("## Counts by risk type")
    lines.append("")
    for risk_type, count in risk_counts.most_common():
        lines.append(f"- {risk_type}: {count}")
    lines.append("")

    lines.append("## Sample rows")
    lines.append("")
    for row in rows[:10]:
        lines.append(f"### {row.get('id', 'unknown')} | {row.get('category', 'unknown')}")
        lines.append("")
        lines.append(f"- Difficulty: {row.get('difficulty', 'unknown')}")
        lines.append(f"- Prompt: {row.get('prompt', '')}")
        lines.append(f"- Expected behavior: {row.get('expected_behavior', '')}")
        lines.append("")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize generated JSONL dataset.")
    parser.add_argument("--input", required=True, help="Path to generated JSONL file.")
    parser.add_argument("--output", required=True, help="Path to Markdown report.")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    rows = load_jsonl(input_path)
    report = make_report(rows, input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote {output_path} for {len(rows)} rows")


if __name__ == "__main__":
    main()
