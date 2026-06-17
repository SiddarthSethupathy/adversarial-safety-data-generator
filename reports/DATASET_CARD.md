# Dataset Card

## Dataset name

Adversarial Safety Data Generator sample dataset

## Purpose

This dataset is intended for LLM safety evaluation, red-team simulation, and alignment research. It contains user-facing adversarial test prompts and expected safe behavior descriptions.

## Intended use cases

- Evaluating refusal behavior
- Evaluating prompt-injection resistance
- Evaluating secret-exfiltration resistance
- Evaluating over-refusal on safe prompts
- Creating inputs for LLM-based safety scoring
- Supporting future RLHF/GRPO experiments

## Not intended for

- Operational cyber abuse
- Real-world targeting guidance
- Weapons or military operational planning
- Privacy invasion or doxxing
- Self-harm instructions
- Medical, legal, or election deception assistance

## Schema

Each row contains:

- `id`: unique row identifier
- `category`: adversarial prompt category
- `difficulty`: easy, medium, or hard
- `risk_type`: broader risk family
- `prompt`: user-facing adversarial test prompt
- `expected_behavior`: safe model behavior expected for the prompt
- `source`: generation source

## Safety notes

The prompts are meant to test model behavior. They should not include detailed operational steps for harmful actions. Generated data should be reviewed before being used in training or evaluation pipelines.

## Current generation method

The first version is template-based. Future versions may add LLM-backed generation through OpenAI, NeMo Data Designer, or another approved provider.
