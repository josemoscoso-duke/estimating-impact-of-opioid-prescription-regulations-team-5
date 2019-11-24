# Import libraries
import pandas as pd
import numpy as np
import pyarrow
import os

# This function will import previously generated DEA parquets and merge with the population data

### Set directory
os.chdir('/Users/ningjiehu/Documents/estimating-impact-of-opioid-prescription-regulations-team-5/20_intermediate_files')

### Input state
state = 'Florida'
state_abbrev = 'FL'

### Read parquet file (choose target state or comparison state)
## Target state
# opioid = pd.read_parquet('EDA_consolidate.parquet'.format(state_abbrev))

## Comparison state
opioid = pd.read_parquet('DEA_comp_{}.parquet'.format(state_abbrev))
opioid

### Choose state to work on
## For target states
# opioid_state = opioid[opioid['BUYER_STATE'] == state_abbrev]

## For Comparision states
opioid_state = opioid.copy()

### Drop duplicated columns
opioid_condensed = opioid_state[['BUYER_COUNTY', 'BUYER_STATE', 'TRANSACTION_YEAR', 'BUYER_MME']].drop_duplicates(subset = ['BUYER_COUNTY', 'BUYER_STATE', 'TRANSACTION_YEAR', 'BUYER_MME'])
opioid_condensed
opioid_condensed['BUYER_STATE'].unique()

### Check if County name matches in two datasets
opioid_condensed['BUYER_COUNTY'].unique()

### If County names need to be renamed
opioid_rename = opioid_condensed.copy()

## Rename for TX
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'DE WITT':'DEWITT'})

## Rename for FL_comparision
opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'DE KALB':'DEKALB'})
opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT CLAIR':'ST. CLAIR'})

## Rename for LA
#opioid_LA = opioid_rename.copy()
#opioid_LA = opioid_LA[opioid_LA['BUYER_STATE'] == 'LA']
#opioid_LA
#opioid_LA['BUYER_COUNTY'] = opioid_LA['BUYER_COUNTY'].astype(str) + ' PARISH'
#opioid_LA
#opioid_rename = opioid_LA.copy()
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT CHARLES PARISH':'ST. CHARLES PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT HELENA PARISH':'ST. HELENA PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT JAMES PARISH':'ST. JAMES PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT LANDRY PARISH':'ST. LANDRY PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT MARTIN PARISH'':''ST. MARTIN PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT MARY PARISH':'ST. MARY PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT TAMMANY PARISH':'ST. TAMMANY PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'ST JOHN THE BAPTIST PARISH':'ST. JOHN THE BAPTIST PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT BERNARD PARISH':'ST. BERNARD PARISH'})
#opioid_rename['BUYER_COUNTY']= opioid_rename['BUYER_COUNTY'].replace({'SAINT MARTIN PARISH':'ST. MARTIN PARISH'})

### If the data doesn't need to be renamed
opioid_rename = opioid_condensed.copy()

### Generate final data for opioid shipment
opioid_final = opioid_rename.loc[~opioid_condensed.duplicated(['BUYER_COUNTY', 'BUYER_STATE', 'TRANSACTION_YEAR'])]
opioid_final

### Function to merge opioid shipment with the population data
def opioid_merge(st):
        # Read population mortality merged dataset
        pop_data = pd.read_csv('{}ControlStateData.csv'.format(state_abbrev))
        pop_data

        state_data = pop_data.copy()
        ## For target states
        # state_data = state_data[state_data['State Abbreviation'] == state_abbrev]
        # state_data

        ## For comparison States
        state_data = state_data[~state_data['State Abbreviation'].isin([state_abbrev])]
        state_data

        ## Subset for unique year and state pop values by dropping duplicates
        state_pop = state_data[['Year','State Population', 'County Name', 'State Abbreviation']].drop_duplicates(subset = ['Year','State Population', 'County Name', 'State Abbreviation'])
        state_pop


        ## Merge on County name/State abbreivation/Year
        full_merged = pd.merge(state_pop, opioid_final, how='outer', left_on = ['County Name', 'State Abbreviation', 'Year'], right_on = ['BUYER_COUNTY', 'BUYER_STATE', 'TRANSACTION_YEAR'], validate = '1:1', indicator=True)
        full_merged

        ## Check if County name matches in two datasets
        test = full_merged[full_merged.Year.isin(['NaN'])]
        test['BUYER_COUNTY'].unique()
        ## Find out the county name in the population data
        state_pop['County Name'].unique()

        ## Fill 0 for nan values in the BUYER_MME
        full_fill = full_merged.copy()
        full_fill['BUYER_MME'] = full_merged['BUYER_MME'].fillna(value = 0).astype(int)
        full_fill.sample(50)

        ## Organize the dataframe by dropping the repeated columns
        merge_final = full_fill.copy()
        merge_final = full_fill.drop(columns = ['BUYER_COUNTY', 'BUYER_STATE', 'TRANSACTION_YEAR', '_merge'])
        merge_final.sample(50)
        return (merge_final)

### Obtain dataframe
opioid_merged_data = opioid_merge(state)
opioid_merged_data.sample(50)
opioid_merged_data['Year']

### Save file to csv
## For target states
#opioid_merged_data.to_csv("{}OpioidData.csv".format(state_abbrev), index = False)

## For comparision states
opioid_merged_data.to_csv("{}ComparisonOpioidData.csv".format(state_abbrev), index = False)
