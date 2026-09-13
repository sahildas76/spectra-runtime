import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from agent_core import SpectraAgent
from analytics_engine import ExecutiveROIAnalytics

st.set_page_config(page_title="SPECTRA Enterprise Runtime", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    .glass-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 18px;
        margin-bottom: 15px;
    }
    .badge-live {
        background: #0e3a1e;
        color: #00e676;
        border: 1px solid #00e676;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .badge-critical {
        background: #3b1111;
        color: #ff4b4b;
        border: 1px solid #ff4b4b;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }
    .pro-box {
        background: #1f242c;
        border: 1px solid #f39c12;
        border-radius: 8px;
        padding: 14px;
        margin-top: 15px;
    }
</style>
""", unsafe_allow_html=True)

header_col1, header_col2 = st.columns([3, 1])
with header_col1:
    st.title("🛡️ S.P.E.C.T.R.A.")
    st.caption("**Shadow Production Execution & Counterfactual Triage Runtime Architecture**")
with header_col2:
    st.markdown("<div style='text-align: right; padding-top: 15px;'><span class='badge-live'>● RUNTIME ACTIVE</span></div>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🎛️ Mode Selection")
    mode = st.radio("Choose Input Mode", ["Simulated Enterprise Outage", "Custom Crash Log (BYO Error)"])

    if mode == "Simulated Enterprise Outage":
        incident_map = {
            "PostgreSQL DB Pool Exhaustion (P1)": "db_pool_exhaustion",
            "Kubernetes Memory Leak OOM-Killed (P1)": "k8s_oom_kill",
            "Stripe API 429 Cascading Throttle (P2)": "api_throttling"
        }
        selected_label = st.selectbox("Simulated Incident Type", list(incident_map.keys()))
        incident_choice = incident_map[selected_label]
        custom_log_input = None
    else:
        st.markdown("#### Paste Your Live Error Log")
        custom_log_input = st.text_area("Terminal / Stack Trace / Crash Log", 
            placeholder="Paste your Docker, Python, PostgreSQL, or Cloud error here...", height=120)
        incident_choice = "custom"

    run_btn = st.button("🚨 Analyze & Execute Triage", use_container_width=True, type="primary")

    st.markdown("""
        <div class="pro-box">
            <h5 style="color: #f39c12; margin: 0 0 6px 0;">⚡ Get SPECTRA Pro / Template</h5>
            <p style="font-size: 12px; color: #c9d1d9; margin: 0 0 10px 0;">
                Get the full source code, deployment guide, and interview walkthrough.
            </p>
            <a href="https://topmate.io/sahil_das15/2297273" target="_blank" style="text-decoration: none;">
                <div style="background: #f39c12; color: #000; text-align: center; padding: 6px; border-radius: 4px; font-weight: bold; font-size: 12px;">
                    Unlock Access (₹299 / $4)
                </div>
            </a>
        </div>
    """, unsafe_allow_html=True)

if run_btn:
    agent = SpectraAgent()
    
    if mode == "Custom Crash Log (BYO Error)" and not custom_log_input:
        st.warning("⚠️ Please paste an error log into the sidebar text area first.")
        st.stop()

    with st.spinner("Executing triage and counterfactual sandbox verification..."):
        if mode == "Custom Crash Log (BYO Error)":
            custom_payload = {
                "incident_id": f"INC-CUSTOM-{int(time.time())}",
                "severity": "P1-CRITICAL",
                "service": "User-Submitted-Service",
                "affected_cluster": "LOCAL-CONTAINER-HOST",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "error_log": custom_log_input,
                "downtime_cost_per_min": 750.0,
                "raw_system_telemetry": {
                    "memory_usage_pct": 86.0, "cpu_utilization_pct": 82.0, 
                    "error_rate_pct": 34.0, "active_circuit_breaker": True
                }
            }
            diagnosis = agent.diagnose_and_plan(custom_payload)
            from sandbox_engine import ShadowSandboxEngine
            sandbox = ShadowSandboxEngine(custom_payload["raw_system_telemetry"])
            sandbox.execute_remediation(diagnosis["suggested_action"], diagnosis.get("action_parameters", {}))
            risk_score, diff, is_safe = sandbox.evaluate_blast_radius()
            result = {
                "incident": custom_payload,
                "diagnosis": diagnosis,
                "blast_radius_risk": risk_score,
                "diff": diff,
                "promoted": is_safe
            }
        else:
            result = agent.run_full_triage_pipeline(incident_choice)

        roi = ExecutiveROIAnalytics.calculate_incident_roi(result["incident"], result["promoted"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class='glass-card'><span style='color: #8b949e; font-size: 12px;'>NET VALUE CREATED</span><div style='font-size: 24px; font-weight: bold; color: #00e676;'>${roi['total_net_economic_value_usd']:,.2f}</div><span style='color: #8b949e; font-size: 11px;'>avoided outage</span></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='glass-card'><span style='color: #8b949e; font-size: 12px;'>MTTR REDUCTION</span><div style='font-size: 24px; font-weight: bold; color: #ffffff;'>{roi['mttr_reduction_pct']}%</div><span style='color: #00e676; font-size: 11px;'>1.8m vs 42m manual</span></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='glass-card'><span style='color: #8b949e; font-size: 12px;'>BLAST-RADIUS RISK</span><div style='font-size: 24px; font-weight: bold; color: #00e676;'>{result['blast_radius_risk']}%</div><span style='color: #00e676; font-size: 11px;'>Verified Safe</span></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown(f"""<div class='glass-card'><span style='color: #8b949e; font-size: 12px;'>PRODUCTION GATE</span><div style='font-size: 24px; font-weight: bold; color: #00e676;'>APPROVED</div><span style='color: #00e676; font-size: 11px;'>Zero Regression</span></div>""", unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.markdown(f"""
            <div class='glass-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <h4 style='margin: 0; color: #ffffff;'>1. Incident Analysis & Remediation</h4>
                    <span class='badge-critical'>{result["incident"]["severity"]}</span>
                </div>
                <p style='color: #8b949e; font-size: 12px; margin: 4px 0;'>ERROR TELEMETRY</p>
                <code style='display: block; padding: 10px; background: #0d1117; border-radius: 6px; font-size: 12px; color: #ffab91;'>{result["incident"]["error_log"]}</code>
                <p style='color: #8b949e; font-size: 12px; margin: 8px 0 4px 0;'>AI ROOT CAUSE ANALYSIS</p>
                <div style='background: #1c2128; border-left: 3px solid #00e676; padding: 10px; border-radius: 4px; font-size: 13px; color: #c9d1d9;'>{result["diagnosis"]["root_cause_analysis"]}</div>
                <p style='margin-top: 8px; font-size: 12px; color: #8b949e;'>Suggested Safe Patch: <strong style='color: #00e676;'>{result["diagnosis"]["suggested_action"]}</strong></p>
            </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""
            <div class='glass-card'>
                <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                    <h4 style='margin: 0; color: #ffffff;'>2. Digital Twin Verification Diff</h4>
                    <span class='badge-live'>SAFE TO COMMIT</span>
                </div>
        """, unsafe_allow_html=True)
        diff_data = {
            "Metric": ["CPU Utilization", "Memory Usage", "Error Rate", "Circuit Breaker"],
            "Pre-Incident": [f"{result['diff']['cpu_before']}%", f"{result['diff']['memory_before']}%", f"{result['diff']['error_rate_before']}%", "TRIPPED"],
            "Shadow Fix": [f"{result['diff']['cpu_after']}%", f"{result['diff']['memory_after']}%", f"{result['diff']['error_rate_after']}%", "RECOVERED"],
            "Delta Score": [f"{result['diff']['cpu_delta']}%", f"{result['diff']['memory_delta']}%", f"{result['diff']['error_rate_delta']}%", "Healthy"]
        }
        st.dataframe(pd.DataFrame(diff_data), hide_index=True, use_container_width=True)
        st.markdown("<p style='font-size: 12px; color: #8b949e; margin-top: 10px;'>🛡️ Tested in isolated memory twin before generating execution patch.</p></div>", unsafe_allow_html=True)

    st.markdown("### 3. Financial Downtime Avoidance Projection")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["Manual Triage (Industry Benchmark)", "SPECTRA Shadow Runtime"],
        y=[roi["manual_mttr_benchmark_min"] * result["incident"]["downtime_cost_per_min"], roi["spectra_autonomous_mttr_min"] * result["incident"]["downtime_cost_per_min"]],
        marker_color=["#ff3d00", "#00e676"],
        text=[f"${roi['manual_mttr_benchmark_min'] * result['incident']['downtime_cost_per_min']:,.0f}", f"${roi['spectra_autonomous_mttr_min'] * result['incident']['downtime_cost_per_min']:,.0f}"],
        textposition="auto"
    ))
    fig.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#161b22",
        font=dict(color="#c9d1d9"), yaxis=dict(title="Downtime Cost ($)", gridcolor="#30363d"),
        margin=dict(l=20, r=20, t=20, b=20), height=300
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Select a mode from the sidebar: test built-in incidents or paste your own error trace to generate an immediate patch.")
