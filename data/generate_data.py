import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)

# Parameters
num_rows = 1000
start_date = datetime(2025, 1, 1)

sources = ["Facebook Ads", "Google Ads", "Organic", "Referral"]
sales_reps = ["Aman", "Riya", "Karan", "Neha"]

data = []

for i in range(num_rows):
    lead_id = i + 1

    created_at = start_date + timedelta(days=random.randint(0, 60))

    source = random.choice(sources)
    sales_rep = random.choice(sales_reps)

    # Funnel logic (realistic drop-offs)

    # Step 1: Demo booking (60% avg)
    demo_booked = np.random.choice([0, 1], p=[0.4, 0.6])

    # Step 2: Demo attendance (only if booked)
    if demo_booked:
        demo_attended = np.random.choice([0, 1], p=[0.5, 0.5])
    else:
        demo_attended = 0

    # Step 3: Conversion (only if attended)
    if demo_attended:
        converted = np.random.choice([0, 1], p=[0.8, 0.2])
    else:
        converted = 0

    # Revenue
    if converted:
        revenue = random.choice([4000, 5000, 6000])
    else:
        revenue = 0

    data.append([
        lead_id,
        source,
        created_at,
        demo_booked,
        demo_attended,
        converted,
        revenue,
        sales_rep
    ])

df = pd.DataFrame(data, columns=[
    "lead_id",
    "source",
    "created_at",
    "demo_booked",
    "demo_attended",
    "converted",
    "revenue",
    "sales_rep"
])

# Save dataset
df.to_csv("data/raw_data.csv", index=False)

print("Dataset generated successfully!")