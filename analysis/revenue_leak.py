import os

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


def biggest_leak_stage(metrics):
    drop_offs = {
        "Booking Drop": 1 - metrics["booking_rate"],
        "Attendance Drop": 1 - metrics["attendance_rate"],
        "Conversion Drop": 1 - metrics["conversion_rate"],
    }
    return max(drop_offs, key=drop_offs.get)


def founder_action_fields(metrics):
    stage = biggest_leak_stage(metrics)
    if stage == "Booking Drop":
        return {
            "stage": stage,
            "problem": "Users are not booking enough demos after entering the funnel.",
            "evidence": (
                f"Demo booking rate is {metrics['booking_rate']:.2%} "
                "against the 60% operating assumption."
            ),
            "action": "Improve landing page CTA, reduce booking friction, and add faster lead follow-up.",
            "owner": "Growth owner with founder review",
        }
    if stage == "Attendance Drop":
        return {
            "stage": stage,
            "problem": "Booked users are not attending demos consistently.",
            "evidence": (
                f"Demo attendance rate is {metrics['attendance_rate']:.2%} "
                "against the 50% operating assumption."
            ),
            "action": (
                "Add WhatsApp reminders, calendar nudges, and reduce the wait "
                "between booking and demo."
            ),
            "owner": "RevOps owner with sales team follow-up",
        }
    return {
        "stage": stage,
        "problem": "Demo attendees are not converting into paid customers at the expected rate.",
        "evidence": (
            f"Conversion rate is {metrics['conversion_rate']:.2%} "
            "against the 20% operating assumption."
        ),
        "action": "Improve the sales pitch, objection handling, pricing clarity, and post-demo follow-up.",
        "owner": "Founder or sales lead",
    }


def build_founder_action_memo(metrics):
    fields = founder_action_fields(metrics)
    expected_impact = (
        f"Closing the current funnel leak could recover up to INR {metrics['revenue_leak']:,.0f} "
        "against the modeled expected revenue baseline."
    )

    memo_lines = [
        "# Founder Action Memo",
        "",
        "## Problem",
        "",
        fields["problem"],
        "",
        "## Evidence",
        "",
        fields["evidence"],
        f"Current revenue leakage estimate: INR {metrics['revenue_leak']:,.0f}.",
        "",
        "## Action",
        "",
        fields["action"],
        "",
        "## Owner",
        "",
        fields["owner"],
        "",
        "## Expected impact",
        "",
        expected_impact,
        "",
    ]
    return "\n".join(memo_lines)


def write_founder_action_memo(metrics, output_path="outputs/founder_action_memo.md"):
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(build_founder_action_memo(metrics))

    if not os.path.isfile(output_path):
        raise RuntimeError(f"Expected founder action memo at {output_path}")
    return output_path


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

    stage = biggest_leak_stage(metrics)

    print("\n===== INSIGHTS =====")
    print(f"Biggest Leak Stage: {stage}")

    if stage == "Booking Drop":
        print("Problem: Users not booking demos")
        print("Fix: Improve landing page CTA, faster lead follow-up")
    elif stage == "Attendance Drop":
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
    memo_path = write_founder_action_memo(metrics)
    print(f"\nFounder action memo written to {memo_path}")


if __name__ == "__main__":
    main()
