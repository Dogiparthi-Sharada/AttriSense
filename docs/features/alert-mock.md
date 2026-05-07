<!--
AttriSense — docs/features/alert-mock.md
Author : Sharada Dogiparthi <dogiparthi.sharada@gmail.com>
Version: 1.0.0
Date   : 2026-05-07
License: MIT — see LICENSE in repo root.
Copyright (c) 2026 Sharada Dogiparthi. All rights reserved.
-->

# Alert Mock

> Demo of the Slack/Teams notification surface. Shows what a manager would receive for their high-risk reports.

![Alert mock](../images/alert.png)

## What you see

- **Manager picker** — dropdown of all manager IDs in the dataset.
- **Mock Slack/Teams message** — formatted card preview with:
  - Manager name + total reports
  - High-risk count + names
  - Top recommended interventions
  - "Open in dashboard" button (mock — no link wired)
- **Digest options** — daily / weekly / monthly cadence selector.

## What it answers

| Question | Where |
|---|---|
| What does the manager actually see? | The mock card |
| Which managers would be alerted today? | Filter manager picker by `high_risk_count > 0` |
| What does each alert cost? | Aggregate across the cohort (a real Slack workspace bills nothing for messages; the cost is human attention) |

## Code path

```
production/streamlit_app.py
  └── _alert_tab(df)
       └── slack_alert_mock.render_alert_mock(df)
            ├── group by manager_id
            ├── compute high_risk reports per manager
            └── render styled Streamlit card
```

[`slack_alert_mock.py`](https://github.com/Dogiparthi-Sharada/AttriSense/blob/main/production/src/attrisense/slack_alert_mock.py) — 70 lines, no external integrations. The "send" button is intentionally a no-op.

## Why a mock and not a real integration

A real Slack integration would require:

- A Slack bot token + scopes.
- A real workspace to post into.
- A way to handle replies / reactions.
- A way to undo / pause alerts.
- An audit trail for compliance.

None of that fits in a portfolio demo. The mock conveys the **product idea** — manager-level rollup with action-taking surface — without the integration overhead.

A real deployment is a `slack_sdk.WebClient` + a `chat.postMessage` call with the same payload the mock already builds.

## Design choices

- **Manager-level, not exec-level** — execs already get the dashboard. Managers get the people-action.
- **Digest, not real-time** — a Slack ping for every new high-risk score becomes noise. Daily / weekly / monthly is the right cadence.
- **Recommended intervention included** — the alert is actionable, not just informational.
- **No employee names in the message body until the manager opens the dashboard** — minimises Slack history surface area for sensitive labels.

## Future: bidirectional flow

The next iteration would have the Slack message accept reactions:

- :thumbsup: "I'll act on this"
- :thumbsdown: "False positive"
- :eyes: "Reviewing"

Reaction events get logged as labelled feedback, feeding back into the next retrain. This is the "human-in-the-loop active learning" pattern. On the [roadmap](../roadmap.md).
