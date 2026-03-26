import pandas as pd

# Load data
df = pd.read_csv("data/raw_data.csv")

# Basic counts
total_leads = len(df)
demo_booked = df["demo_booked"].sum()
demo_attended = df["demo_attended"].sum()
converted = df["converted"].sum()

# Conversion rates
booking_rate = demo_booked / total_leads
attendance_rate = demo_attended / demo_booked if demo_booked else 0
conversion_rate = converted / demo_attended if demo_attended else 0

# Revenue
total_revenue = df["revenue"].sum()

# Expected revenue (if no leaks)
avg_revenue_per_conversion = df[df["converted"] == 1]["revenue"].mean()

expected_conversions = total_leads * 0.6 * 0.5 * 0.2
expected_revenue = expected_conversions * avg_revenue_per_conversion

revenue_leak = expected_revenue - total_revenue

# Print results
print("\n===== FUNNEL METRICS =====")
print(f"Total Leads: {total_leads}")
print(f"Demo Booking Rate: {booking_rate:.2%}")
print(f"Demo Attendance Rate: {attendance_rate:.2%}")
print(f"Conversion Rate: {conversion_rate:.2%}")

print("\n===== REVENUE =====")
print(f"Total Revenue: ₹{total_revenue:,.0f}")
print(f"Expected Revenue: ₹{expected_revenue:,.0f}")
print(f"Revenue Leakage: ₹{revenue_leak:,.0f}")

# Identify biggest drop
drop_offs = {
    "Booking Drop": 1 - booking_rate,
    "Attendance Drop": 1 - attendance_rate,
    "Conversion Drop": 1 - conversion_rate
}

biggest_leak_stage = max(drop_offs, key=drop_offs.get)

print("\n===== INSIGHTS =====")
print(f"Biggest Leak Stage: {biggest_leak_stage}")

if biggest_leak_stage == "Booking Drop":
    print("→ Problem: Users not booking demos")
    print("→ Fix: Improve landing page CTA, faster lead follow-up")

elif biggest_leak_stage == "Attendance Drop":
    print("→ Problem: Users not attending demos")
    print("→ Fix: WhatsApp reminders, calendar nudges, shorter wait time")

else:
    print("→ Problem: Low conversion after demo")
    print("→ Fix: Improve sales pitch, objection handling, pricing clarity")