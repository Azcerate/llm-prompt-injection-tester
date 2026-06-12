# llm-prompt-injection-tester (`pijack`)

A defensive test harness that fires a corpus of **prompt-injection and
jailbreak** payloads at an LLM endpoint and **scores its defenses** — mapped to
**MITRE ATLAS** adversarial-ML techniques. Point it at any model behind a
small adapter and get a repeatable defense-rate metric you can gate CI on.

> **Defensive use only.** This corpus exists to test and harden systems you own
> or are authorized to assess. The harness plants a known canary secret and
> checks whether attacks can extract it.

## Why this matters

Prompt injection is the #1 risk in the OWASP LLM Top 10, and "we added a system
prompt" is not a control until it's tested. This tool gives AI features the same
treatment we give any other attack surface: a payload corpus, a pass/fail
metric, and a CI gate — so a regression in your guardrails fails the build
instead of shipping.

## Install

```bash
pip install -e .
```

## Usage

```bash
# Built-in undefended baseline (should score 0% — proves detection works)
pijack --target echo

# Built-in guarded baseline (input filter + output scrubbing)
pijack --target guarded -o report.md

# Your own endpoint via a custom adapter
pijack --target examples.custom_target:MyTarget

# CI gate: fail if defense rate drops below 80%
pijack --target guarded --fail-under 80
```

## Writing a target adapter

A target is any class with a `send(user_message) -> str` method:

```python
from pijack.targets import Target

class MyTarget(Target):
    name = "my-llm"
    def send(self, user_message: str) -> str:
        # call your real model and return its text response
        ...
```

Run it with `pijack --target your_module:MyTarget`. Keep credentials in env
vars; never commit keys. See [`examples/custom_target.py`](examples/custom_target.py).

## What it tests

8 techniques across direct injection, indirect/poisoned-document injection,
jailbreaks, obfuscation/encoding, payload splitting, and system-prompt
extraction — each mapped to a MITRE ATLAS technique ID. Extend or replace via a
custom corpus YAML (`--corpus`). See [`pijack/payloads/corpus.yaml`](pijack/payloads/corpus.yaml).

## Example output

```
- Payloads run: 8
- Blocked (defense held): 8
- Leaked (attack succeeded): 0
- Defense rate: 100.0%
```

## Frameworks referenced

MITRE ATLAS · OWASP Top 10 for LLM Applications (LLM01 Prompt Injection).

## License

MIT © 2026 Anthony N. Saunders
