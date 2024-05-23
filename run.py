import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt
import openpyxl
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('Kaplan-Meier')

# Function to retrieve data from the Google Excelsheet
def get_data_from_sheet():
    sheet = SHEET.worksheet('ABC')
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

# Prompt user for new data input
new_data = input("Please enter new survival data")
new_data_a = []
new_data_b = []
new_data_c = []

for i in range(13):
    time_a = input("Enter Time for Group A:")
    event_a = input("Enter Event for Group A:")
    new_data_a.append((time_a, event_a))

    time_b = input("Enter Time for Group B:")
    event_b = input("Enter Event for Group B:")
    new_data_b.append((time_b, event_b))

    time_c = input("Enter Time for Group C:")
    event_c = input("Enter Event for Group C:")
    new_data_c.append((time_c, event_c))

# Validate user input (eg., check for valid data types, decimal places, etc.)


#Load the data from the Google Excel sheet into a DataFrame
data = get_data_from_sheet()

# Replace existing data with new user input:
for i in range(13):
    data.loc[(data['Group'] == 'A') & (data.index ==i), ['Time', 'Event']] = [float(new_data_b[i][0]),bool(new_data_b[i][0])]
    data.loc[(data['Group'] == 'B') & (data.index ==i), ['Time', 'Event']] = [float(new_data_b[i][0]),bool(new_data_b[i][0])]
    data.loc[(data['Group'] == 'C') & (data.index ==i), ['Time', 'Event']] = [float(new_data_b[i][0]),bool(new_data_b[i][0])]



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
