# ---------------------------------------------------------------------------
# AttriSense — production/src/attrisense/slack_alert_mock.py
# ---------------------------------------------------------------------------
# Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
# Version: 1.0.0
# Date   : 2026-05-07
# License: MIT — see LICENSE in repo root.
# Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
# ---------------------------------------------------------------------------
"""Slack-style manager alert mock.

Pure UI \u2014 no backend integration. Renders what a "weekly manager
digest" would look like if AttriSense were wired into Slack or Teams.
Used as a screenshot in interviews and as a "what does adoption look
like?" answer for hiring managers.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from attrisense.compare import headline_drivers
from attrisense.identity import to_review_id


def render_alert_mock(df: pd.DataFrame) -> None:
    """Render a mock weekly digest for one manager."""
    st.markdown("#### Slack/Teams Alert Mock (UI only)")
    st.caption(
        "This is a mock-up of what a weekly manager digest would look like "
        "in Slack or Teams. The dashboard does not send messages."
    )

    high_risk = df[df["Risk_Level"] == "High Risk"]
    if high_risk.empty:
        st.info("No high-risk employees in the database \u2014 alert would be skipped.")
        return

    manager_options = (
        high_risk.groupby("Manager_ID")
        .agg(reports=("Emp_ID", "count"))
        .sort_values("reports", ascending=False)
        .head(20)
        .index.tolist()
    )
    if not manager_options:
        st.info("No managers with high-risk reports.")
        return

    selected_manager = st.selectbox("Manager", manager_options, key="alert_manager")
    cohort = (
        high_risk[high_risk["Manager_ID"] == selected_manager]
        .sort_values("Flight_Risk_Probability", ascending=False)
        .head(5)
    )

    with st.container(border=True):
        st.markdown(f"**\u26a0 AttriSense \u2014 Weekly Manager Digest for Manager {selected_manager}**")
        st.caption(f"{len(cohort)} report(s) flagged as High Risk this week.")
        for row in cohort.itertuples():
            drivers = headline_drivers(pd.Series(row._asdict()), top_k=2)
            driver_text = " \u2022 ".join(drivers) if drivers else "drivers unavailable"
            st.markdown(
                f"**{to_review_id(row.Emp_ID)}** — {row.Department} — risk "
                f"{row.Flight_Risk_Probability:.2f}  \n"
                f"_Top drivers:_ {driver_text}"
            )
        col_view, col_ack, col_snooze = st.columns(3)
        with col_view:
            st.button("View details", key="alert_view", disabled=True)
        with col_ack:
            st.button("Mark as reviewed", key="alert_ack", disabled=True)
        with col_snooze:
            st.button("Snooze 1 week", key="alert_snooze", disabled=True)
        st.caption(
            "Buttons are disabled in the mock. A real integration would post "
            "this card to Slack/Teams via webhook and write the manager's "
            "response back to SQLite."
        )
