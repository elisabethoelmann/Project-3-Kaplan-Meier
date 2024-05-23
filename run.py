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

# Your code goes here.

# Load the data from the excel file into a DataFrame
# data = pd.read_excel('excel_data/realdata2.xlsx')

ABC = SHEET.worksheet('ABC')
data = ABC.get_all_values()
print(data)

#Load the data from the Google Excel sheet into a DataFrame
data = get_data_from_sheet()

#Function to process the data and return the DataFrame
def process_data(df):
    #Replace empty cells with NaN
    df = df.replace(",",np.nan)
    # convert 'Time' column to numeric
    df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
    return df

# process the data and store it in a new variable
processed_df = process_data(data)

#print the rownumber and column letter of empty cells
for i, row in enumerate(data):
    for j, cell in enumerate(row):
        if not cell:
            print(f"Empty cell found at row {i+1},column{chr(ord('A') + j)}")

# Function to process the data and return the DataFrame
def process_data(df):
    #convert 'Time' column to numeric
    df['Time'] = pd.to_numeric(df['Time'],errors='coerce')
    return df

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
