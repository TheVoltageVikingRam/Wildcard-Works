import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
# Ensure 'mosfet_id_vds.csv' is in the same folder as this script
df = pd.read_csv('mosfet_id_vds.csv')

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['Vds'], df['Id'], marker='.', linestyle='-', color='b', label='Id vs Vds')

# Add titles and labels
plt.title('Vds vs Id Characteristics')
plt.xlabel('Vds (V)')
plt.ylabel('Id (A)')

# Add grid and legend
plt.grid(True)
plt.legend()

# Save the plot as a PNG file
output_filename = 'mosfet_plot.png'
plt.savefig(output_filename, dpi=300) # dpi=300 ensures high resolution

print(f"Plot saved successfully as {output_filename}")
