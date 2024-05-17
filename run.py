import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import openpyxl

# Your code goes here.

# Load the data from the excel file into a DataFrame
data = pd.read_excel('excel_data/realdata.xlsx')

# Create the Kaplan-Meier object and fit the data

kmf = KaplanMeierFitter()
kmf.fit(data['Time'], data['Event'], label='Overall Survival')

# Split the data by groups
groups = data['Group'].unique()

# Create a new figure
fig,ax = plt.subplots()

# Plot seperate curves for each group
for group in groups:
    group_data = data[data['Group'] == group]
    kmf.fit(group_data['Time'],group_data['Event'], label=group)
    kmf.plot(ax=ax)

# set labels and title for the plot
ax.set_xlabel('Time')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Curve')

# display legend
ax.legend()

# save and display the plot
plt.savefig('km_plot.png')
plt.show()

# Convert 'Time' and 'Event' columns to numeric tyoes if needed
data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
data['Event'] = pd.to_numeric(data['Event'], errors='coerce')

# Drop rows with missing values
data = data.dropna(subset=['Time', 'Event'])

# Calculate the median PFS for each group
median_pfs_group_A = kmf.fit(data[data['Group Value'] == 1]['Time'], data[data['Group Value'] == 1]['Event']).median_survival_time_
median_pfs_group_B = kmf.fit(data[data['Group Value'] == 2]['Time'], data[data['Group Value'] == 2]['Event']).median_survival_time_
median_pfs_group_C = kmf.fit(data[data['Group Value'] == 3]['Time'], data[data['Group Value'] == 3]['Event']).median_survival_time_


# print the result
print("Median PFS for Group A:{:.2f}".format(median_pfs_group_A))
print("Median PFS for Group B:{:.2f}".format(median_pfs_group_B))
print("Median PFS for Group C:{:.2f}".format(median_pfs_group_C))













# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
