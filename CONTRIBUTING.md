# Contributing

Contributions are welcome. This project values correctness, reproducibility, and
clear documentation over feature volume.

## Development setup

```bash
pip install -e . pytest
pytest -q
```

All tests must pass before a change is merged. CI runs the suite on Python 3.9, 3.11,
and 3.12.

## Guidelines

- Keep changes small and focused; one logical change per pull request.
- Add or update tests for any behavioral change.
- Update the README and any affected documentation in the same pull request.
- Framework mappings (where applicable) must cite an authoritative source.
- Run `pytest -q` locally and ensure it is green before opening a PR.

## Reporting issues

Open a GitHub issue with a minimal reproduction, the command you ran, and the observed
versus expected output.

## Security

This is a defensive security tool. Do not submit content that weaponizes the project or
that targets systems you are not authorized to assess. To report a security concern with
the tool itself, open an issue marked **security** or contact the maintainer directly.
