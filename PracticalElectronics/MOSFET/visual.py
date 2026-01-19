import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
# Ensure 'mosfet_id_vds.csv' is in the same folder as this script
df = pd.read_csv('mosfet_id_vds.csv')

# Convert Id from Amperes (A) to milliamperes (mA)
# Assuming the original data was in Amperes
df['Id'] = df['Id'] * 1000

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['Vds'], df['Id'], marker='.', linestyle='-', color='b', label='Id vs Vds')

# Add titles and labels
plt.title('Vds vs Id Characteristics')
plt.xlabel('Vds (V)')
plt.ylabel('Id (mA)') # Updated label to mA

# Add grid and legend
plt.grid(True)
plt.legend()

# Save the plot as a PNG file
output_filename = 'mosfet_plot_mA.png' # Updated filename
plt.savefig(output_filename, dpi=300) 

print(f"Plot saved successfully as {output_filename}")