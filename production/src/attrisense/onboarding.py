"""First-time-user onboarding tour for the AttriSense v2 dashboard.

Streamlit doesn't have a real product-tour widget yet, so the tour is
implemented as a dismissible card stack stored in `st.session_state`.
The user sees one card at a time, clicks Next/Skip, and the choice is
persisted for the remainder of the session.
"""

from __future__ import annotations

from dataclasses import dataclass

import streamlit as st


_SESSION_KEY = "attrisense_onboarding_step"
_DISMISSED_KEY = "attrisense_onboarding_dismissed"


@dataclass(frozen=True)
class TourStep:
    """A single onboarding card."""

    title: str
    body: str
    cta: str


_STEPS: tuple[TourStep, ...] = (
    TourStep(
        title="Welcome to AttriSense",
        body=(
            "AttriSense turns synthetic HR data into retention-risk decisions. "
            "Every employee is scored by a Random Forest model with SHAP "
            "explanations and Cox survival analysis."
        ),
        cta="Start the tour",
    ),
    TourStep(
        title="Executive view first",
        body=(
            "The Executive Dashboard tab shows total workforce, risk bands, "
            "and the departments most at risk. Use it to answer: "
            "'where do I focus this quarter?'"
        ),
        cta="Next: explanations",
    ),
    TourStep(
        title="SHAP explains every score",
        body=(
            "The SHAP Insights tab shows global drivers and per-employee "
            "contributions. Compare Employees side by side under the new "
            "Compare tab to answer 'why is A higher risk than B?'"
        ),
        cta="Next: decisions",
    ),
    TourStep(
        title="Decision tools",
        body=(
            "The Decision Tools tab includes the What-If Simulator, "
            "manager-level rollup, and the cost-of-attrition calculator. "
            "These convert predictions into business actions."
        ),
        cta="Next: causal",
    ),
    TourStep(
        title="Causal uplift recommendations",
        body=(
            "Causal Uplift estimates how much each candidate intervention "
            "(salary lift, manager change) would change the predicted risk. "
            "It moves the dashboard from prediction to prescription."
        ),
        cta="Next: ethics",
    ),
    TourStep(
        title="Responsible AI is built in",
        body=(
            "Limitations & Ethics, the Fairness Audit, and the Model Card "
            "are first-class tabs. Synthetic data caveats, NYC LL144 "
            "alignment, and a no-adverse-decision policy are documented."
        ),
        cta="Finish tour",
    ),
)


def _state(key: str, default: object) -> object:
    """Tiny helper around `st.session_state` defaults."""
    if key not in st.session_state:
        st.session_state[key] = default
    return st.session_state[key]


def render_onboarding_tour() -> None:
    """Render the onboarding tour. Idempotent; safe to call every render."""
    if _state(_DISMISSED_KEY, False):
        return

    step_index = int(_state(_SESSION_KEY, 0))
    step_index = max(0, min(step_index, len(_STEPS) - 1))
    step = _STEPS[step_index]

    with st.container(border=True):
        st.markdown(
            f"**Tour {step_index + 1}/{len(_STEPS)} — {step.title}**"
        )
        st.write(step.body)
        col_next, col_skip, _ = st.columns([1, 1, 4])
        with col_next:
            if st.button(step.cta, key=f"tour_next_{step_index}"):
                if step_index + 1 >= len(_STEPS):
                    st.session_state[_DISMISSED_KEY] = True
                else:
                    st.session_state[_SESSION_KEY] = step_index + 1
                st.rerun()
        with col_skip:
            if st.button("Skip tour", key=f"tour_skip_{step_index}"):
                st.session_state[_DISMISSED_KEY] = True
                st.rerun()


def reset_onboarding_tour() -> None:
    """Public helper for an `Open tour` button in the sidebar."""
    st.session_state[_SESSION_KEY] = 0
    st.session_state[_DISMISSED_KEY] = False
