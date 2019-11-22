# Import libraries
import pandas as pd
import numpy as np
import os

# This function will import previously merged state and mortality data and
# concatenate the dataframes to make plotting death/shipment per capita
# more streamlined

# Change directory
os.chdir("C:/Users/Varun/Documents/MIDS/Fall 2019/IDS 690 - Practical Data Science with Python/Midterm Project/estimating-impact-of-opioid-prescription-regulations-team-5")

# Input state abbreviations
main_state = 'WA' # Change depending on FL, TX, or WA
# Comparison state list
state_list = ['WA','ID','MT','NV','OR']


# Function to read in data and concatenate dataframes
def state_combo(st_list):
    # Initialize dataframe
    all_states = pd.DataFrame()

    # Loop through the states
    for state in state_list:
        state_data = pd.read_csv("20_intermediate_files/{}MortPopData.csv".format(state))
        all_states = pd.concat([all_states,state_data])
    return all_states

# Return combined table
combined_data = state_combo(state_list)
combined_data

# Add column that classifies states as either main policy state or comparison state
combined_data['Policy State'] = np.where(combined_data['State Abbreviation'] == main_state, True, False)
combined_data

# Save concatenated dataframe to csv
combined_data.to_csv("20_intermediate_files/{}ControlStateData.csv".format(main_state), index = False)
