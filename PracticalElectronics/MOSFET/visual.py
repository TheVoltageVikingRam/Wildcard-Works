import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('mosfet_id_vds.csv')

df['Id'] = df['Id'] * 1000

plt.figure(figsize=(10, 6))
plt.plot(df['Vds'], df['Id'], marker='.', linestyle='-', color='b', label='Id vs Vds')

plt.title('Vds vs Id Characteristics')
plt.xlabel('Vds (V)')
plt.ylabel('Id (uA)') 

plt.grid(True)
plt.legend()


output_filename = 'mosfet_plot_mA.png' # Updated filename
plt.savefig(output_filename, dpi=300) 

print(f"Plot saved successfully as {output_filename}")
