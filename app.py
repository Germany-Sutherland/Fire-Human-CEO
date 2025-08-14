import streamlit as st
import time

# -----------------------------
# Basic Config / Page Settings
# -----------------------------
st.set_page_config(
    page_title="Agentic AI CEO — Leadership FMEA",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Predefined classic cases
# -----------------------------
CASES = {
    "Nokia": "Failed to adapt from feature phones to smartphone OS ecosystems (iOS/Android).",
    "Kodak": "Underestimated the shift to digital photography despite inventing it internally.",
    "Blockbuster": "Ignored/late to video streaming disruption and online subscription models.",
    "Sears": "Lost retail share to e-commerce and discounters due to slow digital pivot.",
    "Pan Am": "High fixed costs, deregulation shocks, and financial mismanagement led to collapse."
}

# -----------------------------
# Leadership styles dictionary
# -----------------------------
LEADER_STYLES = {
    "Autocratic Leader Agentic AI Agent CEO": "Decides alone, tight control, speed over consensus.",
    "Democratic Leader Agentic AI Agent CEO": "Seeks participation and consensus, inclusive decision-making.",
    "Laissez-Faire Leader Agentic AI Agent CEO": "Hands-off, relies on team autonomy and initiative.",
    "Transformational Leader Agentic AI Agent CEO": "Drives inspiring vision, change, and innovation.",
    "Transactional Leader Agentic AI Agent CEO": "Targets performance via incentives, KPIs, and compliance.",
    "Servant Leader Agentic AI Agent CEO": "Puts people first, grows teams, builds trust and community.",
    "Charismatic Leader Agentic AI Agent CEO": "Inspires via presence and storytelling; rallies followers.",
    "Situational Leader Agentic AI Agent CEO": "Adapts style to team maturity and task complexity.",
    "Visionary Leader Agentic AI Agent CEO": "Long-term strategic focus; bold bets and roadmaps.",
    "Bureaucratic Leader Agentic AI Agent CEO": "Follows rules and procedures; values consistency."
}

STYLE_BIASES = {
    # These biases nudge FMEA scoring (0–10 scale).
    # Positive => higher risk on that axis, Negative => lower risk on that axis.
    "Autocratic":        {"severity": +1, "occurrence": +1, "detection": -1},
    "Democratic":        {"severity":  0, "occurrence": +1, "detection":  0},
    "Laissez-Faire":     {"severity": +1, "occurrence": +2, "detection": -1},
    "Transformational":  {"severity": +2, "occurrence": +1, "detection": -1},
    "Transactional":     {"severity":  0, "occurrence":  0, "detection": +1},
    "Servant":           {"severity":  0, "occurrence":  0, "detection":  0},
    "Charismatic":       {"severity": +2, "occurrence": +1, "detection": -1},
    "Situational":       {"severity": -1, "occurrence": -1, "detection": +1},
    "Visionary":         {"severity": +2, "occurrence": +1, "detection": -1},
    "Bureaucratic":      {"severity": -1, "occurrence":  0, "detection": +2},
}

# -----------------------------
# Utility: lightweight heuristic FMEA
# -----------------------------
RISKY_KEYWORDS = {
    "merger": (+2, +1, -1), "acquisition": (+2, +1, -1), "layoff": (+2, +2, -1),
    "restructure": (+1, +1, -1), "pivot": (+2, +1, -1), "ai": (+1, +1, -1),
    "cloud": (+1, 0, 0), "shutdown": (+3, +2, -2), "outsourcing": (+1, +1, 0),
    "offshoring": (+1, +1, 0), "automation": (+1, +1, 0), "cybersecurity": (+2, +1, +1),
    "compliance": (+1, 0, +2), "regulation": (+1, 0, +2), "expansion": (+1, +1, -1)
}

def clamp(x, lo=1, hi=10):
    return max(lo, min(hi, int(round(x))))

def base_scores(problem:str, decision:str):
    # Start with moderate base scores
    sev, occ, det = 6, 5, 5
    text = f"{problem} {decision}".lower()
    for kw, (ds, do, dd) in RISKY_KEYWORDS.items():
        if kw in text:
            sev += ds; occ += do; det += dd
    # Simple scale with length (longer often => more complex/risky)
    length_factor = min(len(text) // 200, 3)
    sev += length_factor; occ += length_factor
    return clamp(sev), clamp(occ), clamp(det)

def style_adjusted_scores(sev, occ, det, leader_name:str):
    for key, bias in STYLE_BIASES.items():
        if key in leader_name:
            sev += bias["severity"]
            occ += bias["occurrence"]
            det += bias["detection"]
            break
    return clamp(sev), clamp(occ), clamp(det)

def mitigation_for_style(leader_name:str):
    if "Autocratic" in leader_name:
        return [
            "Create a fast feedback loop (weekly red-team review).",
            "Nominate a devil’s advocate for critical decisions."
        ]
    if "Democratic" in leader_name:
        return [
            "Timebox discussions and set a decision deadline.",
            "Designate a final decision owner to avoid stalemates."
        ]
    if "Laissez-Faire" in leader_name:
        return [
            "Set minimal check-ins (biweekly OKRs).",
            "Install simple dashboards for progress visibility."
        ]
    if "Transformational" in leader_name:
        return [
            "Translate vision into 30-60-90 day milestones.",
            "Pair inspiration with risk & dependency registers."
        ]
    if "Transactional" in leader_name:
        return [
            "Align incentives to long-term value, not vanity metrics.",
            "Audit KPIs quarterly to prevent gaming."
        ]
    if "Servant" in leader_name:
        return [
            "Balance empathy with clear performance gates.",
            "Escalate decisively when business risk rises."
        ]
    if "Charismatic" in leader_name:
        return [
            "Triangulate narratives with data and experiments.",
            "Use pre-mortems to counter optimism bias."
        ]
    if "Situational" in leader_name:
        return [
            "Reassess team readiness every sprint.",
            "Adapt coaching/directing mix as competency changes."
        ]
    if "Visionary" in leader_name:
        return [
            "Back-cast the vision into quarterly deliverables.",
            "Run discovery sprints and kill-switch gates."
        ]
    if "Bureaucratic" in leader_name:
        return [
            "Allow policy exceptions for controlled experiments.",
            "Create a lightweight fast-track for innovations."
        ]
    return ["Establish controls, measure, iterate."]

def failure_modes_text(problem:str, decision:str, leader_name:str):
    return (
        f"Execution gaps, misalignment, and unintended consequences while applying "
        f"the decision through the lens of {leader_name}."
    )

def effects_text():
    return "Delays, cost overruns, quality issues, compliance risks, or missed market opportunities."

def eli5_block(leader_name:str, sev:int, occ:int, det:int):
    return (
        "ELI5: Think of **Severity** as how big the ouch is, **Occurrence** as how often it happens, "
        "and **Detection** as how quickly we can spot it. A higher **RPN** means more care is needed. "
        f"This leader style tilts risks like this: S={sev}, O={occ}, D={det}."
    )

def run_fmea(problem:str, decision:str, leader_name:str, want_eli5:bool):
    sev0, occ0, det0 = base_scores(problem, decision)
    sev, occ, det = style_adjusted_scores(sev0, occ0, det0, leader_name)
    rpn = sev * occ * det  # classic Risk Priority Number

    result = {
        "Failure Mode": failure_modes_text(problem, decision, leader_name),
        "Effects": effects_text(),
        "Severity (S)": sev,
        "Occurrence (O)": occ,
        "Detection (D)": det,
        "RPN = S×O×D": rpn,
        "Mitigation Strategy": mitigation_for_style(leader_name),
    }
    if want_eli5:
        result["ELI5"] = eli5_block(leader_name, sev, occ, det)
    return result

# -----------------------------
# Sidebar Controls
# -----------------------------
with st.sidebar:
    st.header("Settings")
    delay = st.slider("Thinking delay (seconds per agent)", 0.0, 3.0, 1.2, 0.1)
    show_eli5 = st.checkbox("Show ELI5 explanations", value=True)
    compact = st.checkbox("Compact view (hide score details)", value=False)
    st.markdown("---")
    st.subheader("About")
    st.write(
        "This demo is rule-based and lightweight for Streamlit Free. "
        "It simulates 10 leadership agents doing FMEA with explainable, ELI5 output."
    )

# -----------------------------
# Header & Inputs
# -----------------------------
st.title("🤖 Agentic AI CEO — 10 Leadership Styles FMEA")
st.caption("Type a **Problem** and the **Decision taken by the CEO**. Watch 10 agents think in sequence and explain risks + mitigations.")

cols = st.columns([2, 1.2, 1.2, 1.2, 1.2, 1.2])
with cols[0]:
    chosen_case = st.selectbox("Pick a classic case (optional)", [""] + list(CASES.keys()))
with cols[1]:
    use_case_btn = st.button("Use case text")
with cols[2]:
    clear_btn = st.button("Clear inputs")
with cols[3]:
    run_btn_top = st.button("Run FMEA (Top)")
with cols[4]:
    st.write("")  # spacer
with cols[5]:
    st.write("")

# Problem & Decision inputs
default_problem = CASES.get(chosen_case, "") if use_case_btn else ""
problem = st.text_area("Problem", value=default_problem, height=100, placeholder="Describe the business problem…")
decision = st.text_area("Decision taken by CEO", height=100, placeholder="Describe the decision that has been taken…")

if clear_btn:
    problem = ""
    decision = ""
    st.experimental_rerun()

run_btn = st.button("Run FMEA with 10 Leadership Agents") or run_btn_top

# -----------------------------
# Validation
# -----------------------------
if run_btn:
    if not problem.strip() or not decision.strip():
        st.warning("Please provide both **Problem** and **Decision taken by CEO**.")
    else:
        st.success("Running sequential agents…")
        st.markdown("---")
        # Iterate styles in fixed order to ensure consistent UX
        for leader, desc in LEADER_STYLES.items():
            # Thinking placeholder
            think = st.empty()
            think.info(f"⏳ Wait, Our AI CEO Agent is think... ({leader})")
            time.sleep(delay)

            # Replace with results
            think.empty()
            section = st.container()
            with section:
                st.subheader(leader)
                st.caption(desc)

                # Compute result
                result = run_fmea(problem, decision, leader, want_eli5=show_eli5)

                if compact:
                    st.markdown(f"**Failure Mode:** {result['Failure Mode']}")
                    st.markdown(f"**Effects:** {result['Effects']}")
                    st.markdown("**Mitigation Strategy:**")
                    for m in result["Mitigation Strategy"]:
                        st.markdown(f"- {m}")
                    if show_eli5 and "E_
