import pandas as pd
import random
from datetime import datetime, timedelta

# -----------------------------
# CONFIGURATION (INDUSTRY-LIKE)
# -----------------------------
NUM_REQUESTS = 300        # ~300 requests
START_DATE = datetime(2025, 1, 1)
END_DATE = datetime(2025, 4, 1)  # ~3 months

PRIORITY_DISTRIBUTION = {
    "High": 0.15,
    "Medium": 0.55,
    "Low": 0.30
}

STAGES = ["submitted", "in_progress", "resolved", "closed"]

# Typical stage durations by priority (hours)
DURATION_RANGES = {
    "High": {
        "submitted": (0.1, 0.5),
        "in_progress": (0.5, 2),
        "resolved": (1, 3),
        "closed": (0.1, 0.5),
    },
    "Medium": {
        "submitted": (0.2, 1),
        "in_progress": (1, 4),
        "resolved": (2, 6),
        "closed": (0.2, 1),
    },
    "Low": {
        "submitted": (0.5, 2),
        "in_progress": (3, 10),
        "resolved": (6, 20),
        "closed": (0.5, 2),
    }
}

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def choose_priority():
    r = random.random()
    cumulative = 0
    for p, weight in PRIORITY_DISTRIBUTION.items():
        cumulative += weight
        if r <= cumulative:
            return p
    return "Low"

def random_start_time():
    delta = END_DATE - START_DATE
    return START_DATE + timedelta(seconds=random.randint(0, int(delta.total_seconds())))

# -----------------------------
# DATA GENERATION
# -----------------------------
rows = []

for request_id in range(1, NUM_REQUESTS + 1):
    priority = choose_priority()
    current_time = random_start_time()

    for stage in STAGES:
        rows.append([
            request_id,
            stage,
            current_time.strftime("%Y-%m-%d %H:%M"),
            priority
        ])

        min_h, max_h = DURATION_RANGES[priority][stage]
        current_time += timedelta(hours=random.uniform(min_h, max_h))

df = pd.DataFrame(
    rows,
    columns=["request_id", "stage", "timestamp", "priority"]
)

# -----------------------------
# SAVE CSV
# -----------------------------
df.to_csv("data/process_events.csv", index=False)

print("✅ Generated realistic event log data")
print(df.head())
