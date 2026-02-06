import pandas as pd

df = pd.read_csv(r"C:\Users\laksh\Downloads\sample_equipment_data.csv")
total_equipment = len(df)
avg_flowrate = df["Flowrate"].mean()
avg_pressure = df["Pressure"].mean()
avg_temperature = df["Temperature"].mean()
type_distribution = df["Type"].value_counts()

summary = {
    "total_equipment": total_equipment,
    "average_flowrate": avg_flowrate,
    "average_pressure": avg_pressure,
    "average_temperature": avg_temperature,
    "type_distribution": type_distribution.to_dict()
}

print(summary)