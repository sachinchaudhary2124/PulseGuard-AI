import gradio as gr
import pandas as pd
import plotly.express as px
import tempfile
import random

from datetime import datetime, timedelta

from utils.anomaly_detector import detect_anomalies
from agents.root_cause_agent import analyze_root_cause
from agents.recommendation_agent import generate_executive_summary


# =========================================================
# CYBER AI CSS
# =========================================================

custom_css = """

body{
    background:
        radial-gradient(circle at top left, rgba(99,102,241,0.15), transparent 25%),
        radial-gradient(circle at bottom right, rgba(236,72,153,0.12), transparent 25%),
        linear-gradient(135deg,#020617,#0f172a,#111827);

    background-attachment: fixed;
    color:white;
}

.gradio-container{
    background:rgba(15,23,42,0.78)!important;
    backdrop-filter:blur(14px);
    border-radius:24px;
    padding:22px;
    border:1px solid rgba(99,102,241,0.18);
    box-shadow:0 0 30px rgba(99,102,241,0.12);
}

.gr-box{
    border-radius:18px!important;
    border:1px solid rgba(99,102,241,0.22)!important;
    box-shadow:0 0 18px rgba(99,102,241,0.12);
}

button{
    background:linear-gradient(90deg,#6366f1,#8b5cf6)!important;
    color:white!important;
    border:none!important;
    border-radius:12px!important;
    font-weight:bold!important;
}

h1,h2,h3{
    text-shadow:0 0 12px rgba(99,102,241,0.6);
}

table, textarea, select{
    background-color:rgba(15,23,42,0.95)!important;
    color:white!important;
}

"""


# =========================================================
# LIVE LOG GENERATOR
# =========================================================

def generate_live_logs():

    endpoints = [
        "/login",
        "/payment",
        "/orders",
        "/inventory",
        "/search",
        "/profile"
    ]

    logs = []

    now = datetime.now()

    for i in range(30):

        endpoint = random.choice(endpoints)

        if random.random() < 0.35:

            status_code = random.choice([500,503,504])

            response_time = random.randint(3000,7000)

        else:

            status_code = 200

            response_time = random.randint(100,1200)

        logs.append({

            "timestamp":
                (now + timedelta(seconds=i*5)).isoformat(),

            "endpoint": endpoint,

            "status_code": status_code,

            "response_time_ms": response_time
        })

    return logs


# =========================================================
# REPORT GENERATOR
# =========================================================

def generate_report(summary, report):

    content = f"""

PULSEGUARD AI INCIDENT REPORT
=====================================

EXECUTIVE SUMMARY
-------------------------------------

{summary}


ROOT CAUSE ANALYSIS
-------------------------------------

{report}

"""

    file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt",
        mode="w",
        encoding="utf-8"
    )

    file.write(content)

    file.close()

    return file.name


# =========================================================
# MAIN ENGINE
# =========================================================

def run_monitoring(selected_endpoint="All"):

    logs = generate_live_logs()

    anomalies = detect_anomalies(logs)

    df = pd.DataFrame(anomalies)

    if df.empty:

        return 0,0,0,0,None,pd.DataFrame(),"No issues","No analysis",None

    # Severity
    df["severity"] = df["status_code"].apply(

        lambda x:
            "Critical" if x >= 503
            else "High" if x >= 500
            else "Medium"
    )

    # KPIs
    total = len(df)

    critical = len(df[df["severity"] == "Critical"])

    avg_response = round(
        df["response_time_ms"].mean(),
        2
    )

    affected = df["endpoint"].nunique()

    # Chart
    chart_df = pd.DataFrame(logs)

    if selected_endpoint != "All":

        chart_df = chart_df[
            chart_df["endpoint"] == selected_endpoint
        ]

    fig = px.line(

        chart_df,

        x="timestamp",

        y="response_time_ms",

        color="endpoint",

        title="API Response Time Monitoring",

        template="plotly_dark"
    )

    fig.update_layout(

        paper_bgcolor="#050816",

        plot_bgcolor="#050816",

        font_color="white"
    )

    # AI Analysis
    reports = []

    for anomaly in anomalies[:3]:

        reports.append(
            analyze_root_cause(anomaly)
        )

    ai_report = "\n\n".join(reports)

    executive_summary = generate_executive_summary(anomalies)

    report_file = generate_report(

        executive_summary,

        ai_report
    )

    return (

        total,

        critical,

        avg_response,

        affected,

        fig,

        df,

        executive_summary,

        ai_report,

        report_file
    )


# =========================================================
# DASHBOARD UI
# =========================================================

with gr.Blocks(

    theme=gr.themes.Soft(),

    title="PulseGuard AI",

    css=custom_css

) as app:

    gr.Markdown("""

# 🚨 PulseGuard AI

### AI-Powered API Failure Detection & Debugging System

#### Autonomous AI Observability Platform

---

🟢 AI Monitoring ACTIVE

🔍 Live anomaly detection enabled

🧠 AI Root Cause Engine running

⚡ Real-time infrastructure intelligence enabled

---

""")

    (
        total,
        critical,
        avg_response,
        affected,
        chart,
        table,
        summary,
        report,
        file
    ) = run_monitoring("All")

    if critical > 0:

        gr.Markdown(f"""

## 🔴 CRITICAL INCIDENT ALERT

{critical} critical infrastructure issues detected.

Immediate engineering attention required.

""")

    else:

        gr.Markdown("""

## 🟢 SYSTEM HEALTHY

No critical incidents detected.

""")

    # KPI ROW
    with gr.Row():

        total_box = gr.Number(
            label="🚨 Total Anomalies",
            value=total
        )

        critical_box = gr.Number(
            label="🔴 Critical Issues",
            value=critical
        )

        response_box = gr.Number(
            label="⚡ Avg Response Time",
            value=avg_response
        )

        endpoint_box = gr.Number(
            label="🌐 Affected Endpoints",
            value=affected
        )

    # Filter
    endpoint_filter = gr.Dropdown(

        choices=[
            "All",
            "/login",
            "/payment",
            "/orders",
            "/inventory",
            "/search",
            "/profile"
        ],

        value="All",

        label="🔍 Filter Endpoint"
    )

    # Chart
    latency_plot = gr.Plot(value=chart)

    # Summary
    gr.Markdown("## 📊 Executive Incident Summary")

    summary_box = gr.Textbox(

        value=summary,

        lines=10,

        label="AI Executive Summary"
    )

    # Table
    gr.Markdown("## 🚨 Detected Anomalies")

    anomaly_table = gr.Dataframe(

        value=table,

        interactive=False
    )

    # Analysis
    gr.Markdown("## 🧠 AI Incident Analysis")

    report_box = gr.Textbox(

        value=report,

        lines=18,

        label="AI Root Cause Analysis"
    )

    # Download
    file_box = gr.File(

        value=file,

        label="📥 Download Incident Report"
    )

    # Refresh
    refresh_btn = gr.Button(
        "🔄 Refresh Live Monitoring"
    )

    refresh_btn.click(

        fn=run_monitoring,

        inputs=[endpoint_filter],

        outputs=[
            total_box,
            critical_box,
            response_box,
            endpoint_box,
            latency_plot,
            anomaly_table,
            summary_box,
            report_box,
            file_box
        ]
    )


# =========================================================
# LAUNCH APP
# =========================================================

app.launch(server_name="0.0.0.0", server_port=7860)