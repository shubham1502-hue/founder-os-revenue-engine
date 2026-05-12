import pandas as pd


REQUIRED_COLUMNS = {
    "lead_id",
    "source",
    "created_at",
    "demo_booked",
    "demo_attended",
    "converted",
    "revenue",
    "sales_rep",
}


def validate_csv_schema(df, input_path="data/raw_data.csv"):
    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_columns:
        expected = ", ".join(sorted(REQUIRED_COLUMNS))
        missing = ", ".join(missing_columns)
        raise ValueError(
            f"{input_path} is missing required columns: {missing}. "
            f"Expected columns: {expected}"
        )


def load_revenue_data(input_path="data/raw_data.csv"):
    df = pd.read_csv(input_path)
    validate_csv_schema(df, input_path)
    return df


def analyze_revenue_leak(df):
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

    return {
        "total_leads": total_leads,
        "booking_rate": booking_rate,
        "attendance_rate": attendance_rate,
        "conversion_rate": conversion_rate,
        "total_revenue": total_revenue,
        "expected_revenue": expected_revenue,
        "revenue_leak": revenue_leak,
    }


def print_revenue_report(metrics):
    print("\n===== FUNNEL METRICS =====")
    print(f"Total Leads: {metrics['total_leads']}")
    print(f"Demo Booking Rate: {metrics['booking_rate']:.2%}")
    print(f"Demo Attendance Rate: {metrics['attendance_rate']:.2%}")
    print(f"Conversion Rate: {metrics['conversion_rate']:.2%}")

    print("\n===== REVENUE =====")
    print(f"Total Revenue: INR {metrics['total_revenue']:,.0f}")
    print(f"Expected Revenue: INR {metrics['expected_revenue']:,.0f}")
    print(f"Revenue Leakage: INR {metrics['revenue_leak']:,.0f}")

    drop_offs = {
        "Booking Drop": 1 - metrics["booking_rate"],
        "Attendance Drop": 1 - metrics["attendance_rate"],
        "Conversion Drop": 1 - metrics["conversion_rate"],
    }

    biggest_leak_stage = max(drop_offs, key=drop_offs.get)

    print("\n===== INSIGHTS =====")
    print(f"Biggest Leak Stage: {biggest_leak_stage}")

    if biggest_leak_stage == "Booking Drop":
        print("Problem: Users not booking demos")
        print("Fix: Improve landing page CTA, faster lead follow-up")

    elif biggest_leak_stage == "Attendance Drop":
        print("Problem: Users not attending demos")
        print("Fix: WhatsApp reminders, calendar nudges, shorter wait time")

    else:
        print("Problem: Low conversion after demo")
        print("Fix: Improve sales pitch, objection handling, pricing clarity")


def main():
    try:
        df = load_revenue_data()
    except ValueError as exc:
        print(f"Invalid CSV schema: {exc}")
        raise SystemExit(1) from exc

    metrics = analyze_revenue_leak(df)
    print_revenue_report(metrics)


if __name__ == "__main__":
    main()
