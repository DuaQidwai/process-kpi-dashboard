# Process Performance & Efficiency Insights

An end-to-end analytics dashboard designed to evaluate process efficiency, identify bottlenecks, and assess SLA compliance across request priorities using event-level operational data.

---

##  Project Overview

Operational teams often rely on event logs to understand how work moves through a system, where delays occur, and whether service-level agreements (SLAs) are being met. This project simulates how internal analytics teams translate raw process data into actionable insights using interactive dashboards rather than static reports.

Using timestamped workflow events, the dashboard measures request cycle times, surfaces bottlenecks across process stages, evaluates performance variability, and assesses SLA compliance by priority. The goal is to highlight where operational risk exists and where targeted process improvements would have the greatest impact.

---

## Objectives

This project was built to:

- Analyze end-to-end process performance using event-level data
- Identify workflow stages that contribute most to delays
- Measure variability and tail-risk beyond simple averages
- Evaluate SLA compliance based on request priority
- Demonstrate how analytics supports operational decision-making

---

## Key Questions Addressed

- Where does time accumulate across the process lifecycle?
- Which workflow stages act as the primary bottlenecks?
- How stable is performance over time?
- How large is the gap between average performance and worst-case (P90) outcomes?
- Do higher-priority requests consistently meet tighter SLAs?
- Where do SLA breaches introduce operational risk?

---

## Data Description

The dataset represents synthetic event-level logs for individual requests moving through a multi-stage process. Each request progresses through the following stages:

- `submitted`
- `in_progress`
- `resolved`
- `closed`

Each event includes:
- `request_id` — unique identifier for a request
- `stage` — process stage
- `timestamp` — time the request entered that stage
- `priority` — business priority (`High`, `Medium`, `Low`)

Synthetic data is used to simulate realistic operational behavior while avoiding sensitive information.

---

## Methodology

### Cycle Time Calculation
Cycle time is calculated at the request level by summing the time spent between consecutive process stages from submission to closure.

### Bottleneck Identification
Average time spent in each stage is computed to identify where requests spend the most time waiting. The stage with the highest average duration is flagged as the primary bottleneck.

### Variability & Risk
In addition to average cycle time, the 90th percentile (P90) is calculated to capture tail-risk and long-delay cases that disproportionately impact service reliability.

### SLA Evaluation
Service-level agreements are defined based on request priority:

| Priority | SLA Target |
|--------|-----------|
| High | 4 hours |
| Medium | 12 hours |
| Low | 24 hours |

Each request is evaluated against its priority-specific SLA to determine compliance. SLA metrics are used to highlight where delays translate into contractual or operational risk.

---

## Analysis

### End-to-End Cycle Time Performance
Cycle time was calculated at the request level by summing the time elapsed between consecutive process stages from submission through closure. This metric captures the full customer-facing duration of a request and serves as the primary indicator of operational efficiency. While average cycle time provides a useful baseline, it masks significant variability across individual request. As a result, percentile-based metrics were incorporated to better understand performance risk and long-tail behavior.

### Variability and Tail Risk (P90 Analysis)
In addition to average cycle time, the 90th percentile (P90) was calculated to capture worst-case performance scenarios. The gap between the mean and P90 cycle times indicates the presence of long-tail delays that disproportionately impact service reliability. Although average performance appears relatively stable, elevated P90 values suggest that a subset of requests experience signficantly longer resolution time. These outliers are operationally meaningful, as they are more likely to result in SLA breaches, escalations, and negative customer impact

### Bottleneck Identification
To identify process bottlenecks, the average time spent in each workflow stage was computed across all requests. The stage with the highest average duration was flagged as the primary bottleneck.

Results indicate that the resolved stage contributes the most to overall cycle time. This suggests that delays occur not during active processing, but during post-resolution handoffs such as validation, approval, or formal closure.

This finding is particularly important, as it implies that efficiency gains may be achieved by improving downstream workflows rather than increasing processing capacity.

### Performance Trends Over Time
Cycle time trends were analyzed by aggregating request completion times by date. This temporal view enables identification of performance drift, short-term spikes, or sustained degradation.

Observed fluctuations in average cycle time over time suggest that performance is influenced by factors such as workload variability, capacity constraints, or process dependencies. Continuous monitoring is therefore necessary to detect emerging risks before they materially impact SLA compliance.

### Priority-Based Performance Analysis
Requests were segmented by priority level to assess whether higher-urgency requests consistently receive faster resolution. Average cycle times were compared across High, Medium, and Low priority categories.

Results indicate that higher-priority requests do not always resolve significantly faster than lower-priority ones. This suggests potential misalignment between prioritization policies and actual execution, or capacity constraints that limit the effectiveness of prioritization during peak demand.

This finding highlights an opportunity to refine priority handling mechanisms to better align operational outcomes with business intent.

### SLA Evaluation and Compliance Risk
Service-level agreements (SLAs) were defined based on request priority and evaluated against total request cycle time:

- High Priority: 4 hours
- Medium Priority: 12 hours
- Low Priority: 24 hours

Each request was assessed for SLA compliance by comparing its cycle time against the appropriate priority-based threshold.

While overall SLA compliance remains relatively high, tighter SLAs expose meaningful risk concentrated in higher-priority workflows. SLA breaches tend to align with long-tail cases identified in the P90 analysis, reinforcing the relationship between variability and service reliability.

This demonstrates that improving SLA performance requires addressing variability and bottlenecks, not simply improving average throughput.

---

## Dashboard Highlights

### Key Performance Indicators
- Average cycle time
- Total requests processed
- Primary bottleneck stage
- P90 cycle time
- SLA compliance rate

### Visual Analysis
- **Process Bottleneck Analysis:** Average time spent in each workflow stage
- **Performance Trends:** Cycle time trends over completion dates
- **Priority Analysis:** Cycle time comparison across request priorities

### Operational Insights
Concise, decision-oriented insights are embedded directly in the dashboard to guide interpretation without overwhelming the viewer with excessive text.

---

## Tech Stack

- **Python** – core programming language
- **Pandas** – data transformation and aggregation
- **Plotly** – interactive data visualization
- **Streamlit** – dashboard framework

---

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/process-kpi-dashboard.git
   cd process-kpi-dashboard
