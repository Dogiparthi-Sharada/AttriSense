<!--
AttriSense — CONTRIBUTING.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Contributing to AttriSense

Thanks for considering a contribution. AttriSense aims to be a **reference example** of explainable, fair, resilient HR analytics — so every PR is judged against that bar.

## Before you open a PR

1. **Tests pass.**

   ```bash
   cd production && pytest tests/ -v
   ```

   All 31 tests must be green. PRs that drop coverage will be asked to add tests.

2. **Lint passes.**

   ```bash
   ruff check .
   ```

3. **Docs updated.** If you touched a feature, update its [`docs/features/<name>.md`](docs/features/). If you touched the model, update the [model card](docs/ethics/model-card.md).

4. **No secrets committed.** `.env`, real PATs, real customer data — none of these belong in a commit. The repo's `.gitignore` covers `.env`; double-check `git status` before you push.

5. **Conventional commit messages.** `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`. Helps us auto-generate the changelog.

## What we'll accept

- Bug fixes (always welcome).
- New dashboard tabs that align with the [roadmap](docs/roadmap.md#-next-in-priority-order).
- Better tests — coverage lift, edge cases, mutation testing.
- Documentation improvements, especially in `docs/learn/` and `docs/troubleshooting.md`.
- Performance fixes that come with a benchmark.
- Accessibility improvements (color contrast, keyboard nav, screen reader labels).

## What we won't accept

See [docs/roadmap.md — Deliberately not on the list](docs/roadmap.md#-deliberately-not-on-the-list). PRs in any of those areas will be closed with a link.

In short: **no auto-mitigated fairness**, **no MLflow / Airflow / dbt / GraphQL**, **no mobile app**, **no second model framework**.

## How to develop locally

1. Clone + create a Python 3.11 venv (see [docs/quickstart.md](docs/quickstart.md)).
2. `pip install -e "production[dev]"` (editable install with dev extras).
3. Make your change.
4. Run `pytest production/tests/ -v` and `ruff check`.
5. Run the dashboard manually: `make -C production run`. Smoke-test the tab you changed.
6. Commit. Open a PR against `main`.

## Code style

- **Python**: PEP 8 + `ruff` defaults. Type hints encouraged but not mandatory.
- **Imports**: stdlib → third-party → local, alphabetised inside each group.
- **Docstrings**: only on public module-level functions/classes. Inline comments preferred over noisy docstrings on small functions.
- **Tests**: `pytest`, parametrise where it helps. One assertion per test where reasonable.

## Reviewing fairness/ethics changes

Any PR touching `production/src/attrisense/fairness.py`, the model card, or the fairness policy gets an extra round of review from the maintainer. Allow extra time. We'd rather slow a fairness PR than ship a regression.

## Communication

Open an issue first if your PR is bigger than ~200 lines or touches the model. Saves both of us time.

---

By submitting a contribution you agree it's released under the project's [MIT license](LICENSE).
