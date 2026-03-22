import pandas as pd
import numpy as np

df1 = pd.read_csv('data/bcsc_risk_factors_summarized1_092020.csv')
df2 = pd.read_csv('data/bcsc_risk_factors_summarized2_092020.csv')
df3 = pd.read_csv('data/bcsc_risk_factors_summarized3_092020.csv')

df = pd.concat([df1, df2, df3], ignore_index=True)
print(f"Combined shape: {df.shape}")
print(f"Total patients represented: {df['count'].sum():,}")

print("\nColumn value counts:")
for col in df.columns:
    print(f"\n{col}:")
    print(df[col].value_counts().sort_index().to_string())