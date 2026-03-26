import pandas as pd

# Load data
df = pd.read_csv("data/raw_data.csv")

# Funnel metrics
total_leads = len(df)
demo_booked = df["demo_booked"].sum()
demo_attended = df["demo_attended"].sum()
converted = df["converted"].sum()

booking_rate = demo_booked / total_leads
attendance_rate = demo_attended / demo_booked if demo_booked else 0
conversion_rate = converted / demo_attended if demo_attended else 0

# Identify problem areas
problems = []

problems.append({
    "task": "Improve demo booking rate",
    "impact": 8 if booking_rate < 0.6 else 5,
    "urgency": 7,
    "effort": 5
})

problems.append({
    "task": "Improve demo attendance",
    "impact": 9 if attendance_rate < 0.6 else 6,
    "urgency": 8,
    "effort": 4
})

problems.append({
    "task": "Improve sales conversion",
    "impact": 10 if conversion_rate < 0.25 else 6,
    "urgency": 9,
    "effort": 6
})

# Create DataFrame
tasks_df = pd.DataFrame(problems)

# Priority Score
tasks_df["priority_score"] = (tasks_df["impact"] * tasks_df["urgency"]) / tasks_df["effort"]

# Sort tasks
tasks_df = tasks_df.sort_values(by="priority_score", ascending=False)

print("\n===== PRIORITY TASK LIST =====")
print(tasks_df)
print("\n===== FOUNDER RECOMMENDATION =====")

top_task = tasks_df.iloc[0]["task"]

print(f"FOCUS AREA: {top_task}")

if "booking" in top_task.lower():
    print("→ Fix landing page + reduce friction")
    print("→ Add instant lead follow-up")

elif "attendance" in top_task.lower():
    print("→ Add WhatsApp reminders")
    print("→ Reduce time gap between booking & demo")

else:
    print("→ Train sales team")
    print("→ Improve demo script & objection handling")