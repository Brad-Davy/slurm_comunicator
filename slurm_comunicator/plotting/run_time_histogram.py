import pandas as pd
import matplotlib.pyplot as plt

cm = 1/2.54 
plt.rcParams.update({'font.size': 12})


file_path = '../run_time_2025-02-25.xlsx'
df = pd.read_excel(file_path)


list_of_dicts = df.to_dict(orient='records')

column_name = 'number_of_cores'  



print(f'50/% of jobs finished within: {df.quantile(0.50).values[0]:.1f} minutes.')
print(f'90/% of jobs finished within: {df.quantile(0.90).values[0]:.1f} minutes.')
print(f'99/% of jobs finished within: {df.quantile(0.99).values[0]:.1f} minutes.')
plt.figure(figsize=(12*cm, 12*cm))
plt.yscale('log')
plt.hist(df, bins=50, edgecolor='black')
plt.title('Run time of jobs')
plt.xlabel('Run time (Minutes)')
plt.ylabel('Frequency')
plt.grid(True)
plt.tight_layout()
plt.savefig('img/core_useage_histogram.svg', dpi=300)
plt.show()
