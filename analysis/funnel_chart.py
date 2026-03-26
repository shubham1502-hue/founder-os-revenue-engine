import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw_data.csv")

total = len(df)
booked = df["demo_booked"].sum()
attended = df["demo_attended"].sum()
converted = df["converted"].sum()

stages = ["Leads", "Booked", "Attended", "Converted"]
values = [total, booked, attended, converted]

plt.figure()
plt.plot(stages, values, marker='o')

for i, v in enumerate(values):
    plt.text(i, v, str(v), ha='center')

plt.title("Funnel Drop-Off")
plt.xlabel("Stage")
plt.ylabel("Users")

plt.savefig(".../assets/funnel_chart.png")
plt.show()