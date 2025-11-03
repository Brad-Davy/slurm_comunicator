import pandas as pd
import matplotlib.pyplot as plt

cm = 1 / 2.54
plt.rcParams.update({"font.size": 12})


file_path = "../../../output_2025-02-18.xlsx"
df = pd.read_excel(file_path)


list_of_dicts = df.to_dict(orient="records")

column_name = "number_of_cores"


plt.figure(figsize=(12 * cm, 12 * cm))
plt.hist(df[column_name], bins=30, edgecolor="black")
plt.title("Number of Cores Used")
plt.xlabel("Number of Cores")
plt.ylabel("Frequency")
plt.grid(True)
plt.tight_layout()
plt.savefig("img/core_useage_histogram.svg", dpi=300)
plt.show()
