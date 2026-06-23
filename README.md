# Adversarial Safety Data Generator

This repository generates structured adversarial safety-evaluation prompts for LLM red-teaming and alignment research.

The goal is to create data that helps test whether a model can handle jailbreaks, prompt injection, secret extraction attempts, cyber-misuse requests, defense-sensitive requests, privacy risks, and over-refusal traps safely.

This repo is intended for defensive evaluation and safety research. It does not provide operational cyber, military, or harmful instructions. Each generated row includes an `expected_behavior` field describing what a safe model response should do.

## Dataset schema

Each generated JSONL row has this structure:

```json
{
  "id": "adv_000001",
  "category": "prompt_injection",
  "difficulty": "medium",
  "risk_type": "instruction_hierarchy_attack",
  "prompt": "User-facing adversarial test prompt.",
  "expected_behavior": "Safe behavior the model should follow.",
  "source": "template_generator_v1"
}
```

## Quick start

Generate a small dataset:

```bash
python scripts/generate_dataset.py --num-examples 100 --output data/sample_generated_prompts.jsonl
```

Validate the dataset:

```bash
python scripts/validate_jsonl.py --input data/sample_generated_prompts.jsonl
```

Create a summary report:

```bash
python scripts/summarize_dataset.py --input data/sample_generated_prompts.jsonl --output reports/GENERATION_REPORT.md
```

## Current categories

- `system_prompt_extraction`
- `jailbreak_instruction_override`
- `prompt_injection`
- `secret_exfiltration`
- `cyber_misuse`
- `vulnerability_discovery_misuse`
- `military_or_defense_sensitive_request`
- `privacy_doxxing`
- `election_misinformation`
- `self_harm`
- `medical_unsafe_advice`
- `legal_deception`
- `over_refusal_trap`
- `safe_normal_prompt`



## OpenAI-backed generation

The repo has two generation modes:

1. `scripts/generate_dataset.py` — local template-based generation. This works without an API key.
2. `scripts/generate_with_openai.py` — OpenAI-backed generation. This requires `OPENAI_API_KEY`.

Do not put your OpenAI key in the code or commit it to GitHub. Set it in your terminal instead:

```bash
export OPENAI_API_KEY="your_key_here"
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run a small dry run first:

```bash
python scripts/generate_with_openai.py --dry-run --num-examples 5
```

Then generate a small preview file:

```bash
python scripts/generate_with_openai.py --num-examples 5 --output data/openai_generated_prompts_preview.jsonl
```

Validate it:

```bash
python scripts/validate_jsonl.py --input data/openai_generated_prompts_preview.jsonl
```

Create a report:

```bash
python scripts/summarize_dataset.py --input data/openai_generated_prompts_preview.jsonl --output reports/OPENAI_GENERATION_REPORT.md
```

The OpenAI-backed generator reads the same `data/seed_categories.jsonl` file as the template generator. Instead of using local templates, it sends the category, risk type, difficulty, description, and expected behavior to OpenAI and asks for one fresh safety-evaluation prompt.

## Intended use

Use this data to:

- test model refusal behavior
- test prompt-injection resistance
- test over-refusal behavior
- create safety evaluation reports
- prepare inputs for LLM-based safety scoring
- support future RLHF/GRPO experiments

## Not intended use

This repo should not be used to create operational harmful instructions, malware guidance, real targeting guidance, or privacy-invasive content.
