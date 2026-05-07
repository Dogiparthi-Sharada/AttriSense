<!--
AttriSense — docs/contributing.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Contributing

> The project welcomes bug fixes, doc improvements, and small new features.

## Quick start

1. Fork the repo.
2. Create a branch: `git checkout -b fix/short-description`.
3. Run the tests: `cd production && make test` — should be 31 passing.
4. Make your change.
5. Run `make check` (lint + format + typecheck + test).
6. Commit with a short, imperative message: `Fix KeyError in compare tab`.
7. Open a PR. Reference the issue number if there is one.

## What's a good first contribution

| Easy | Medium | Hard |
|---|---|---|
| Fix a typo in docs | Add a new gold question | Add a Postgres adapter |
| Add a docstring | Add a chart to an existing tab | Add a new dashboard tab |
| Improve a test's assertions | Add a new fairness metric | Migrate to a different LLM |

## Coding conventions

- **Format**: `black .` from the repo root.
- **Lint**: `ruff check .` — no warnings.
- **Type hints**: required for all public functions in `production/src/attrisense/`.
- **Imports**: stdlib → third-party → local, alphabetised within each group. Ruff handles this.
- **Docstrings**: required for public functions; short, descriptive, no fluff.
- **Tests**: required for new code paths.

## Tests

```bash
cd production
make test                # 31 tests should pass
pytest -v                # verbose mode
pytest -k headline       # only tests matching "headline"
pytest --cov=src/attrisense --cov-report=term-missing
```

If you add a new module, add a `test_<module>.py` next to it. Pattern:

```python
"""Tests for the new feature."""
from attrisense.new_module import new_function


def test_returns_expected_value() -> None:
    """The function should return X when given Y."""
    assert new_function("Y") == "X"
```

## Documentation

If your change is user-facing, update the docs:

- New feature → add a page under `docs/features/`.
- Config change → update `docs/operations/configuration.md`.
- New error path → add an entry to `docs/troubleshooting.md`.

To preview docs locally:

```bash
cd production
make docs-serve
# OR
mkdocs serve
```

Browse to `http://localhost:8000`.

## Commit style

Short imperative subject lines. No emoji. No prefixes like `[FIX]`.

```
Good: Fix KeyError on Compare tab when SHAP_Explained is int
Bad : Fixed bug
Bad : [FIX] 🐛 fixed compare bug because shap_explained was an int and you cant boolean index with int (issue #42)
```

If the change needs more context, put it in the body, not the subject.

## PR description

Include:

1. What changed (one paragraph).
2. Why (one paragraph — link the issue if there is one).
3. How tested (`make test` is the minimum).
4. Screenshots if it's a UI change.

Don't ship a 500-line PR. Break into smaller PRs that can be reviewed one at a time.

## Branch / version policy

- **`main`** — always green. CI passes, dashboard runs.
- **Feature branches** — squash-merge into `main` once approved.
- **Tags** — `v2.0.0` style. Bump version in `production/pyproject.toml` and `production/src/attrisense/__init__.py`.

## Code of conduct

Be kind. Assume good faith. Disagree about ideas, not about people.

If you witness or experience harassment in this project's spaces (issues, PRs, discussions), please report it to the maintainer (currently the repo owner via GitHub DM).

## License

By contributing, you agree your contributions are licensed under the same license as the project.
