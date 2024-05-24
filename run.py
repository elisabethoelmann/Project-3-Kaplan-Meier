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
# Validation of user input (valid data for "time" 0-15 with max.1 decimal place and "event" valid data either 0 or 1)
new_data = input("Please enter new survival data")
new_data_a = []
new_data_b = []
new_data_c = []

for i in range(13):
    while True:
        time_a = input("Enter Time for Group A:")
        if 0 <=float(time_a) <= 15 and time_a.count('.') <= 1:
            break
        else:
            print("Invalid input. Please enter a number between 0-15 with 1 decimal place")

    while True:
        event_a = input("Enter Event for Group A:")
        if event_a.isdigit() and int(event_a) in[0,1]:
            break
        else:
            print("invalid input. Please enter either 0 or 1.")
   
    new_data_a.append((time_a, event_a))

    while True:
        time_b = input("Enter Time for Group B:")
        if 0 <=float(time_b) <=15 and time_b.count('.') <= 1:
            break
        else:
            print("Invalid input. Please enter a number between 0-15 with 1 decimal place")
    while True:
        event_b = input("Enter Event for Group B:")
        if event_b.isdigit() and int(event_b) in[0,1]:
            break
        else:
            print("Invalid input. Please enter either 0 or 1")

    new_data_b.append((time_b, event_b))


    while True:
        time_c = input("Enter Time for Group C:")
        if 0 <=float(time_c) <= 15 and time_c.count('.') <= 1:
            break
        else:
            print("Invalid input. Please enter a number between 0-15 with 1 decimal place.")

    while True:
        event_c = input("Enter Event for Group C:")
        if event_c.isdigit() and int(event_c) in[0,1]:
            break
        else:
            print("Invalid input. Please enter either 0 or 1.")

    new_data_c.append((time_c, event_c))

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
event = 'Event'

group_A_data = data[data['Group Value'] == 1]
group_B_data = data[data['Group Value'] == 2]
group_C_data = data[data['Group Value'] == 3]

median_pfs_group_A = kmf.fit(group_A_data['Time'], group_A_data[event]).median_survival_time_
median_pfs_group_B = kmf.fit(group_B_data['Time'], group_B_data[event]).median_survival_time_
median_pfs_group_C = kmf.fit(group_C_data['Time'], group_C_data[event]).median_survival_time_


# print the result
print("Median PFS for Group A:{:.2f}".format(median_pfs_group_A))
print("Median PFS for Group B:{:.2f}".format(median_pfs_group_B))
print("Median PFS for Group C:{:.2f}".format(median_pfs_group_C))













# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
