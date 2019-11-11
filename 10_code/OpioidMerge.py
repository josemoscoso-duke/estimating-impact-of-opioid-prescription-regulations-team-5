# Import libraries
import pandas as pd
import numpy as np
import pyarrow

# Input state
state = 'Texas'
state_abbrev = 'TX'

# Read parquet file
opioid = pd.read_parquet("../20_intermediate_files/EDA_consolidate.parquet")
opioid

opioid_state = opioid[opioid['BUYER_STATE'] == state_abbrev]
opioid_state

def opioid_merge(st):
    # Read population mortality merged dataset
    state_data = pd.read_csv("../20_intermediate_files/{}MortPopData.csv".format(state_abbrev))
    state_data
    # Subset for unique year and state pop values by dropping duplicates
    state_pop = state_data[['Year','State Population']].drop_duplicates(subset = ['Year','State Population'])
    state_pop

    # Merge on year with year/population data
    full_merged = opioid_state.merge(state_pop, how = "left", left_on = ["TRANSACTION_YEAR"],
    right_on = ["Year"], indicator = True, validate = "m:m")
    full_merged = full_merged.drop(columns = ['Year','_merge'])
    full_merged
    return(full_merged)

# Obtain dataframe
opioid_merged_data = opioid_merge(state)
opioid_merged_data

# Save file to csv
opioid_merged_data.to_csv("../20_intermediate_files/{}OpioidData.csv".format(state_abbrev), index = False)
