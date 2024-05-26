import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
from lifelines.plotting import add_at_risk_counts
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

# First part of the code to draw a Kaplan-Meier curve form the existing data in the Google sheet and calculated mPFS 

# Function to retrieve data from the Google Excelsheet
def get_data_from_sheet():
    sheet = SHEET.worksheet('ABC')
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df

#Load the data from the Google Excel sheet into a DataFrame
data = get_data_from_sheet()

# Function to plot the Kaplan-Meier curve
def plot_kaplan_meier_curve(data):
    # Create the Kaplan-Meier object and fit the data
    kmf = KaplanMeierFitter()
    kmf.fit(data['Time'], data['Event'], label='Overall Survival')
    return kmf

# Call the plot_kaplan_meier_curve function with the loaded data
plot_kaplan_meier_curve(data)
kmf = plot_kaplan_meier_curve(data)

# Split the data by groups
groups = data['Group'].unique()

# Create a new figure
fig,ax = plt.subplots()

# Plot seperate curves for each group
for group in groups:
    group_data = data[data['Group'] == group]
    # Use the existing kmf object to fit and plot the curve
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

# Convert 'Time' and 'Event' columns to numeric types if needed
data['Time'] = pd.to_numeric(data['Time'], errors='coerce')
data['Event'] = pd.to_numeric(data['Event'], errors='coerce')

# Drop rows with missing values
data = data.dropna(subset=['Time', 'Event'])

# Function to calculate the median PFS for each group
def calculate_median_pfs(data):
    event = 'Event'
    group_A_data = data[data['Group Value'] == 1]
    group_B_data = data[data['Group Value'] == 2]
    group_C_data = data[data['Group Value'] == 3]

    kmf = KaplanMeierFitter()
    median_pfs_group_A = kmf.fit(group_A_data['Time'], group_A_data[event]).median_survival_time_
    median_pfs_group_B = kmf.fit(group_B_data['Time'], group_B_data[event]).median_survival_time_
    median_pfs_group_C = kmf.fit(group_C_data['Time'], group_C_data[event]).median_survival_time_

    return median_pfs_group_A, median_pfs_group_B, median_pfs_group_C

# Calculate mPFS for each group
median_pfs_group_A, median_pfs_group_B, median_pfs_group_C = calculate_median_pfs(data)

# print the result
print("Median PFS for Group A:{:.2f}".format(median_pfs_group_A))
print("Median PFS for Group B:{:.2f}".format(median_pfs_group_B))
print("Median PFS for Group C:{:.2f}".format(median_pfs_group_C))

# 2nd part of the code to enable the user to enter new data, re-plot the Kaplan-Meier curve with new data and feed the new data back into the Google sheet

# Prompt user for new data input
# Validation of user input (valid data for "time" 0-15 with max.1 decimal place and "event" valid data either 0 or 1)
data_str = input("Enter your data here:\n")
new_data_a = [(None, None)] * 13
new_data_b = [(None, None)] * 13
new_data_c = [(None, None)] * 13

for i in range(13):
    while True:
        time_a = input("Enter Time for Group A:")
        if 0 <= float(time_a) <= 15 and time_a.count('.') <= 1:
            break
        else:
            print("Invalid input. Please enter a number between 0-15 with 1 decimal place")

    while True:
        event_a = input("Enter Event for Group A:")
        if event_a.isdigit() and int(event_a) in [0,1]:
            new_data_a[i] = (time_a, event_a)
            break
        else:
            print("invalid input. Please enter either 0 or 1.")

    while True:
        time_b = input("Enter Time for Group B:")
        if 0 <= float(time_b) <= 15 and time_b.count('.') <= 1:
            break
        else:
            print("Invalid input. Please enter a number between 0-15 with 1 decimal place")
    while True:
        event_b = input("Enter Event for Group B:")
        if event_b.isdigit() and int(event_b) in [0,1]:
            new_data_b[i] = (time_b, event_b)
            break
        else:
            print("Invalid input. Please enter either 0 or 1")

       
    while True:
        time_c = input("Enter Time for Group C:")
        if 0 <= float(time_c) <= 15 and time_c.count('.') <= 1:
            break
        else:
            print("Invalid input. Please enter a number between 0-15 with 1 decimal place.")

    while True:
        event_c = input("Enter Event for Group C:")
        if event_c.isdigit() and int(event_c) in [0,1]:
            new_data_c[i] = (time_c, event_c)
            break
        else:
            print("Invalid input. Please enter either 0 or 1.")


# Replace existing data with new user input for all rows:
# Update the data in the appropriate index range
for i, (data_a, data_b, data_c) in enumerate(zip(new_data_a, new_data_b, new_data_c)):
    start_index_a = 2 + i
    end_index_a = 14 + i
    start_index_b = 15 + i
    end_index_b = 27 + i
    start_index_c = 28 + i
    end_index_c = 40 + i
    
    if end_index_a <= len(data):
        data.loc[(data['Group'] == 'A') & (data.index >= start_index_a) & (data.index <= end_index_a), ['Time', 'Event']] = [float(data_a[0]), int(data_a[1])]
    else:
        print("Index out of range for Group A")
    
    if end_index_b <= len(data):
        data.loc[(data['Group'] == 'B') & (data.index >= start_index_b) & (data.index <= end_index_b), ['Time', 'Event']] = [float(data_b[0]), int(data_b[1])]
    else:
        print("Index out of range for Group B")

    if end_index_c <= len(data):
        data.loc[(data['Group'] == 'C') & (data.index >= start_index_c) & (data.index <= end_index_c), ['Time', 'Event']] = [float(data_c[0]), int(data_c[1])]
    else:
        print("Index out of range for Group C")


# up-date the Google Excel sheet with the modified data
worksheet = SHEET.worksheet('ABC')
worksheet.update([data.columns.values.tolist()] + data.values.tolist())

