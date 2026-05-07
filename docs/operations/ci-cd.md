<!--
AttriSense — docs/operations/ci-cd.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# CI / CD

> The automation that catches bugs before they reach `main`.

## What runs on every push

[`.github/workflows/ci.yml`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/.github/workflows/ci.yml) runs:

1. **Setup** — Python 3.11, install `production[dev]`.
2. **Lint** — `ruff check .` (replaces flake8 + isort).
3. **Format** — `black --check .`.
4. **Type check** — `mypy production/src/attrisense`.
5. **Test** — `pytest production/tests/ -v`.

A failure on any step blocks the green checkmark. No tests are skipped on CI vs. local.

## The 31 tests

| Test file | What it covers | Tests |
|---|---|---|
| `test_config.py` | All config paths exist; thresholds are sane | 4 |
| `test_compare.py` | `headline_drivers` + the SHAP_Explained bug regression | 3 |
| `test_fairness.py` | Four-fifths rule logic; group metrics; pass/fail | 5 |
| `test_eval.py` | Gold-question loader; `_normalise_rows`; report shape | 4 |
| `test_multilingual_rag.py` | `HashingEmbeddings` returns unit vectors of correct dim | 3 |
| `test_nl_sql_fallback.py` | TF-IDF ranker; gold question execution | 3 |
| `test_nl_sql_validator.py` | SELECT-only allow-list; mutating SQL blocked | 6 |
| `conftest.py` | Shared fixtures (DataFrames, paths) | (no tests) |

## Running locally

```bash
cd production
make test
```

Expected:

```
======== 31 passed in 4.23s ========
```

For coverage:

```bash
make test-cov
# or
pytest --cov=src/attrisense --cov-report=term-missing tests/
```

## Pre-commit hook

Optional but recommended:

```bash
cd production
pip install pre-commit
pre-commit install
```

Now `git commit` runs lint + format + a basic test smoke check before accepting the commit. Bypass with `git commit --no-verify` (don't make a habit of it).

## Adding a new test

```python
# production/tests/test_my_thing.py
"""Tests for the new feature."""

from attrisense.my_thing import my_function


def test_my_function_returns_expected_value() -> None:
    """The function should return X when given Y."""
    assert my_function("Y") == "X"
```

`pytest` auto-discovers anything matching `test_*.py`. No registration needed.

## What's NOT in CI yet

- **Coverage gate** — should be ≥ 70% before merge. Currently informational only.
- **Build the docker image** — would catch Dockerfile drift. Listed in [roadmap.md](../roadmap.md).
- **MkDocs build** — to catch broken links in docs.
- **Smoke-test the dashboard** — Playwright load the homepage, click each tab.

These are easy adds when you have a second person reviewing PRs and the cost of a missed regression starts to bite.

## Branch protection

Recommended for the `main` branch:

| Rule | Why |
|---|---|
| Require PR before merge | Forces review |
| Require CI green | Don't merge red |
| Require linear history | `git log` stays readable |
| Require signed commits | Trust the `Author` field |

These are settings on the GitHub repo page — not in code.

## Release process (future)

Currently AttriSense doesn't tag releases. When it does:

1. Bump version in `production/src/attrisense/__init__.py` and `production/pyproject.toml`.
2. Update `CHANGELOG.md` at the repository root.
3. `git tag v2.1.0 && git push --tags`.
4. CI builds + signs the docker image, publishes to GHCR with the tag.
5. GitHub Release auto-generated from the tag annotation.

For now, the project ships from `main` directly. Pin to a commit SHA if you need stability.
