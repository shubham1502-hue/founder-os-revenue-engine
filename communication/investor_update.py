import pandas as pd

# Load data
df = pd.read_csv("data/raw_data.csv")

# Metrics
total_revenue = df["revenue"].sum()
total_leads = len(df)
demo_booked = df["demo_booked"].sum()
demo_attended = df["demo_attended"].sum()
converted = df["converted"].sum()

booking_rate = demo_booked / total_leads
attendance_rate = demo_attended / demo_booked if demo_booked else 0
conversion_rate = converted / demo_attended if demo_attended else 0

# Identify biggest problem
drop_offs = {
    "Booking": 1 - booking_rate,
    "Attendance": 1 - attendance_rate,
    "Conversion": 1 - conversion_rate
}

biggest_issue = max(drop_offs, key=drop_offs.get)

# Generate update
print("\n===== INVESTOR UPDATE =====\n")

print("Key Metrics:")
print(f"- Revenue: ₹{total_revenue:,.0f}")
print(f"- Booking Rate: {booking_rate:.2%}")
print(f"- Attendance Rate: {attendance_rate:.2%}")
print(f"- Conversion Rate: {conversion_rate:.2%}")

print("\nKey Problem:")
if biggest_issue == "Booking":
    print("- Low demo bookings reducing top-of-funnel efficiency")
elif biggest_issue == "Attendance":
    print("- Significant drop-off in demo attendance impacting conversions")
else:
    print("- Low post-demo conversion affecting revenue realization")

print("\nActions This Week:")
if biggest_issue == "Attendance":
    print("- Implement WhatsApp + email reminders")
    print("- Reduce delay between booking and demo")
    print("- Introduce reschedule nudges")

elif biggest_issue == "Booking":
    print("- Improve landing page CTA")
    print("- Faster lead follow-up")

else:
    print("- Improve sales scripts")
    print("- Train sales team on objection handling")

print("\nFocus:")
print(f"- Fixing {biggest_issue.lower()} to unlock next growth milestone")
