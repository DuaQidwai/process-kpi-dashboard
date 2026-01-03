import streamlit as st
import pandas as pd
import plotly.express as px

SLA_HOURS = {
    "High": 4,
    "Medium": 12,
    "Low": 24
}

# Page Config

st.set_page_config(
    layout="wide",
    page_title="Process Performance & Efficiency Insights"
)

# Global Styling
st.markdown("""
<style>
html, body, [class*="st-"] {
    background-color: #0b1220 !important;
    color: #9ca3af;
}

.stApp {
    background-color: #0b1220 !important;
}

.block-container {
    padding-left: 4rem;
    padding-right: 4rem;
    padding-top: 2rem;
}

.stApp h1 {
    font-size: 2.7rem;
    color: #28dea7;
    font-weight: 700;
}

.stApp h2 {
    font-size: 1.6rem;
    color: #739fe6;
    font-weight: 600;
}

.stApp h3 {
    font-size: 1.2rem;
    color: #c7d2fe;
    font-weight: 600;
}

.stApp p {
    font-size: 1.1rem;
    color: #c3d8fa;
}

.stCaption {
    font-size:10rem;
    color: #c3d8fa;
}


div[data-testid="metric-container"] {
    background-color: #111827;
    border-radius: 16px;
    padding: 16px;
    border: 1px solid #1f2937;
}

div[data-testid="metric-container"] span {
    font-size: 1.8rem;
    color: #28dea7;
    font-weight: 700;
}

.section {
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("Process Performance & Efficiency Insights")
st.caption(
    "Analyzing process efficiency using event logs to identify bottlenecks, trends, and improvement opportunities."
)

# Load & Prepare Data
df = pd.read_csv("data/process_events.csv")
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values(by=["request_id", "timestamp"])

df["next_timestamp"] = df.groupby("request_id")["timestamp"].shift(-1)
df["stage_duration_hours"] = (
    df["next_timestamp"] - df["timestamp"]
).dt.total_seconds() / 3600

durations = df.dropna(subset=["stage_duration_hours"])

# Cycle Time Dataset
completed = df[df["stage"] == "closed"][["request_id", "timestamp"]]
completed = completed.rename(columns={"timestamp": "completion_time"})

cycle_times = (
    durations.groupby("request_id")["stage_duration_hours"]
    .sum()
    .reset_index()
    .merge(completed, on="request_id")
)

cycle_times = cycle_times.merge(
    df[["request_id", "priority"]].drop_duplicates(),
    on="request_id",
    how="left"
)

# SLA Evaluation

# Assign SLA target based on priority
cycle_times["sla_target_hours"] = cycle_times["priority"].map(SLA_HOURS)

# Determine whether SLA was met
cycle_times["sla_met"] = (
    cycle_times["stage_duration_hours"] <= cycle_times["sla_target_hours"]
)


# Metrics
avg_cycle_time = cycle_times["stage_duration_hours"].mean()
p90_cycle_time = cycle_times["stage_duration_hours"].quantile(0.9)
total_requests = cycle_times["request_id"].nunique()

bottleneck_stage = (
    durations.groupby("stage")["stage_duration_hours"]
    .mean()
    .idxmax()
)

# SLA Metrics
overall_sla_compliance = cycle_times["sla_met"].mean() * 100

sla_by_priority = (
    cycle_times
    .groupby("priority")["sla_met"]
    .mean()
    .reset_index()
)

sla_by_priority["sla_met"] = sla_by_priority["sla_met"] * 100


# KPI Card
st.markdown('<div class="card section">', unsafe_allow_html=True)
st.markdown("## Key Performance Indicators")

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Average Cycle Time", f"{avg_cycle_time:.2f} hrs")
k2.metric("Requests Processed", total_requests)
k3.metric("Primary Bottleneck", bottleneck_stage)
k4.metric("P90 Cycle Time", f"{p90_cycle_time:.2f} hrs")
k5.metric("SLA Compliance", f"{overall_sla_compliance:.1f}%")


st.markdown('</div>', unsafe_allow_html=True)

# Charts Data
stage_avg = (
    durations.groupby("stage")["stage_duration_hours"]
    .mean()
    .reset_index()
)

fig_bar = px.bar(
    stage_avg,
    x="stage",
    y="stage_duration_hours",
    template="plotly_dark"
)


cycle_times["completion_date"] = cycle_times["completion_time"].dt.date

daily_trend = (
    cycle_times.groupby("completion_date")["stage_duration_hours"]
    .mean()
    .reset_index()
)

fig_line = px.line(
    daily_trend,
    x="completion_date",
    y="stage_duration_hours",
    markers=True,
    template="plotly_dark"
)

cycle_by_priority = (
    cycle_times.groupby("priority")["stage_duration_hours"]
    .mean()
    .reset_index()
)

fig_priority = px.bar(
    cycle_by_priority,
    x="priority",
    y="stage_duration_hours",
    template="plotly_dark"
)

fig_bar.update_layout( showlegend=False, plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", )
fig_bar.update_traces(marker_color="#28dea7")

fig_line.update_layout( showlegend=False, plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", )
fig_line.update_traces(marker_color="#28dea7")

fig_priority.update_layout( showlegend=False, plot_bgcolor="#0b1220", paper_bgcolor="#0b1220", )
fig_priority.update_traces(marker_color="#28dea7")

# 2x2 GRID (ALL CHARTS)
st.markdown('<div class="section">', unsafe_allow_html=True)

# ---------- ROW 1 ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Process Bottleneck Analysis")
    st.caption("Average time spent in each process stage")
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Performance Trends Over Time")
    st.caption("Average cycle time across completion dates")
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- ROW 2 ----------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Performance by Priority")
    st.caption("Comparing average cycle time across request priorities")
    st.plotly_chart(fig_priority, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("## Additional Analysis")
    #.caption("Reserved for future insights")
    st.markdown(""" 
• **Resolved** is the primary bottleneck, indicating delays between work completion and formal closure  
• While average cycle time appears stable, **P90 values highlight tail-risk driven SLA breaches**  
• Higher-priority requests do not consistently meet tighter SLAs, suggesting prioritization gaps  
• Monitoring SLA compliance alongside bottlenecks enables targeted operational improvements
""")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Raw Data
with st.expander("View underlying event log data"):
    st.dataframe(df)
