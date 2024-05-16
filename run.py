import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter
import matplotlib.pyplot as plt

# Your code goes here.

# Create my data frame
data = pd.DataFrame({
    'Time': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
    'Event': [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1],
    'Group': ['Group A', 'Group A', 'Group A', 'Group A', 'Group B', 'Group B', 'Group B', 'Group B', 'Group B', 'Group B', 'Group B']
   })

# Create the KaplanMeier object and fit the data

kmf = KaplanMeierFitter()
kmf.fit(data['Time'], data['Event'], label='Overall Survival')

# plot the KaplanMeier curve

fig, ax = plt.subplots()
kmf.plot(ax=ax)
ax.set_xlabel('Time')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Curve')
plt.savefig('km_plot.png')










# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
