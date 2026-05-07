"""Tests for the read-only NL\u2192SQL guardrails.

We import the validators directly from the original `natural_language_sql`
module so the production tests pin the contract of the existing dashboard.
"""

from __future__ import annotations

import pytest

# `natural_language_sql._validate_read_only_sql` is private but stable. Import
# it explicitly so any future rename is caught by the test suite.
import natural_language_sql as nlsql


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT * FROM workforce_predictions",
        "select count(*) from workforce_predictions",
        "WITH t AS (SELECT 1) SELECT * FROM t",
    ],
)
def test_read_only_select_is_allowed(sql: str) -> None:
    """SELECT and WITH queries must pass validation."""
    nlsql._validate_read_only_sql(sql)


@pytest.mark.parametrize(
    "sql",
    [
        "INSERT INTO workforce_predictions VALUES (1)",
        "UPDATE workforce_predictions SET Base_Salary = 0",
        "DELETE FROM workforce_predictions",
        "DROP TABLE workforce_predictions",
        "ALTER TABLE workforce_predictions ADD COLUMN evil INT",
        "PRAGMA writable_schema = 1",
        "ATTACH DATABASE 'evil.db' AS bad",
    ],
)
def test_mutating_sql_is_blocked(sql: str) -> None:
    """All mutating or schema-changing SQL must raise."""
    with pytest.raises(ValueError):
        nlsql._validate_read_only_sql(sql)


def test_multi_statement_blocked() -> None:
    """Stacked statements must be rejected."""
    with pytest.raises(ValueError):
        nlsql._validate_read_only_sql("SELECT 1; DELETE FROM workforce_predictions")


def test_clean_sql_strips_markdown() -> None:
    """`_clean_sql` must remove markdown fences and `SQLQuery:` prefixes."""
    raw = "```sql\nSQLQuery: SELECT 1;\n```"
    assert nlsql._clean_sql(raw) == "SELECT 1"
