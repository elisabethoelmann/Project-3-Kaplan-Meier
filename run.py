import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import openpyxl

# Your code goes here.

# Load the data from the excel file into a DataFrame
data = pd.read_excel('excel_data/exampledata.xlsx')

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















# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
