import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('mosfet_id_vds.csv')

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(df['Vds'], df['Id'], marker='.', linestyle='-', color='b', label='Id vs Vds')

# Add titles and labels
plt.title('Vds vs Id Characteristics')
plt.xlabel('Vds (V)')
plt.ylabel('Id (A)')

# Add a grid for better readability
plt.grid(True)
plt.legend()

# Show the plot
plt.show()
