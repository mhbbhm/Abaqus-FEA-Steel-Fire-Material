import numpy as np
import pandas as pd

T = [20, 100, 200, 300, 400, 500, 600, 700, 800]    # Temperature Degree unit
f = [1, 1, 1, 1, 1, 1, 14/15, 13/15, 0.8]   # Steel Residual yield factor
E = 200     # Steel Elastic Modulus 'GPa'
Ve = 0.33   # Steel Poissons ratio
Fy = 420   # Steel Yield Strength 'MPa'
eu = 0.15       # Steel Ultimate strain

Es = ()
Fs = ()

for temp in T:
    Es += ((E*1000, Ve, temp),)

for temp, rate in zip(T, f):
    e = np.linspace(((Fy * rate) / (E * 1000)), eu, 10)
    St = Fy * rate * (1 + e)
    et = np.log(1 + e) - np.log(1 + ((Fy * rate) / (E * 1000)))
    
    for s, e_val in zip(St, et):
        Fs += ((s, e_val, temp),)

# Create DataFrame
data = {'Steel Properties': ['Elastic Modulus (MPa)', 'Poissons Ratio', 'Temperature (°C)'],
        'Values': Es}
Es_df = pd.DataFrame(data['Values'], columns=data['Steel Properties'])

data = {'Stress-Strain Data': ['Stress (MPa)', 'Strain', 'Temperature (°C)'],
        'Values': Fs}
Fs_df = pd.DataFrame(data['Values'], columns=data['Stress-Strain Data'])

# Combine DataFrames horizontally
combined_df = pd.concat([Es_df, Fs_df], axis=1)

# Write DataFrame to Excel
with pd.ExcelWriter(f'Abaqus_FEA_Fire_Material_Steel_{Fy}_MPa.xlsx') as writer:
    combined_df.to_excel(writer, sheet_name=f'Combined_{Fy}_MPa', index=False)