# Import libraries
import pandas as pd
import numpy as np
import os

# BEFORE STARTING: download state population data from this link https://data.ers.usda.gov/reports.aspx?ID=17827
# and adjust the csv to have the following columns: FIPS, County name, RUC Code, Pop. 1990,
# Pop. 2000, Pop. 2010, Pop. 2018, Change 2010-2018. After downloading, you must delete the image textbox and then manually
# readjust the columns so that it is in this format. Save as "StatePopulationReportCleaned.csv" and add
# to 00/source/Population in Github. States that are two words, like New York, need to be
# saved as follows: New YorkPopulationReportCleaned.csv
# See template of "WashingtonPopulationReportCleaned.csv" in source files for proper csv format

# Change directory
os.chdir("C:/Users/Varun/Documents/MIDS/Fall 2019/IDS 690 - Practical Data Science with Python/Midterm Project/estimating-impact-of-opioid-prescription-regulations-team-5")

# Input state name and abbreivation
state = 'Florida'
state_abbrev = 'FL'

# Function to clean population and mortality data and then merge the two dataframes
def pop_mort_merge(st):
    # Import state population data
    pop = pd.read_csv("00_source/Population/{}PopulationReportCleaned.csv".format(st), sep = ',')

    # Drop extra column and recheck dataframe
    pop = pop.drop(columns = "Unnamed: 8")
    pop

    # Rename FIPS column
    pop = pop.rename(columns = {"FIPS*":"FIPS"})

    # Population estimation
    pop_pop = pop.copy()
    # Convert columns to float types (replace commas and %)
    pop_pop['Pop. 1990'] = pop_pop['Pop. 1990'].str.replace(',', '').astype(int)
    pop_pop['Pop. 2000'] = pop_pop['Pop. 2000'].str.replace(',', '').astype(int)
    pop_pop['Pop. 2010'] = pop_pop['Pop. 2010'].str.replace(',', '').astype(int)
    pop_pop['Pop. 2018'] = pop_pop['Pop. 2018'].str.replace(',', '').astype(int)
    pop_pop['Change 2010-18'] = pop_pop['Change 2010-18'].str.replace('%','').astype(float)
    pop_pop
    # Assume linear increase in population from 2000 to 2018 (find change per year)
    avg_change_10 = round((pop_pop['Pop. 2010'] - pop_pop['Pop. 2000'])/10).astype(int)
    avg_change_18 = round((pop_pop['Pop. 2018'] - pop_pop['Pop. 2010'])/8).astype(int)
    # Create columns of population for each year
    year_list = list(range(2001,2019))
    for year in year_list:
        if year < 2010:
            pop_pop['Pop. ' + str(year)] = pop_pop['Pop. ' + str(year-1)] + avg_change_10
        elif year == 2010:
            pop_pop['Pop. ' + str(year)] = pop_pop['Pop. ' + str(year)]
        else:
            pop_pop['Pop. ' + str(year)] = pop_pop['Pop. ' + str(year-1)] + avg_change_18
    # Drop and reorder
    pop_pop = pop_pop.drop(columns = ["RUC code","Pop. 1990","Change 2010-18"])
    pop_pop = pop_pop[['FIPS', 'County name', 'Pop. 2000','Pop. 2001', 'Pop. 2002',
    'Pop. 2003', 'Pop. 2004', 'Pop. 2005', 'Pop. 2006', 'Pop. 2007',
    'Pop. 2008', 'Pop. 2009', 'Pop. 2010','Pop. 2011', 'Pop. 2012', 'Pop. 2013',
    'Pop. 2014', 'Pop. 2015', 'Pop. 2016','Pop. 2017', 'Pop. 2018']]
    # Rename columns to be years
    new_columns = []
    for i in pop_pop.columns:
        if i[0] == 'P':
            pop_pop = pop_pop.rename(columns = {i:i[5:]})
    pop_pop.head()

    # Reshape population table to have following columns: FIPS, County, Year, population
    # Create year column list
    var_columns = []
    for i in pop_pop.columns:
        if i[0] == '2':
            var_columns.append(i)
    pop_pop_reshaped = pd.melt(pop_pop, id_vars = ['FIPS','County name'],
    value_vars = var_columns, var_name = 'Year', value_name = 'Population')
    pop_pop_reshaped

    # Convert to proper types
    pop_pop_reshaped['Year'] = pop_pop_reshaped['Year'].astype(int)
    pop_pop_reshaped['Population'] = pop_pop_reshaped['Population'].astype(int)
    pop_pop_reshaped['County name'] = pop_pop_reshaped['County name'].astype(str)
    pop_pop_reshaped.dtypes
    pop_pop_reshaped

    # Create frame of total state population
    pop_total = pop_pop_reshaped.copy()
    pop_total = pop_pop_reshaped[pop_pop_reshaped['County name'] == st]
    pop_total
    pop_total = pop_total.rename(columns = {"Population":"State Population"})
    pop_total

    # Remove popshington from original reshaped dataframe
    pop_pop_reshaped2 = pop_pop_reshaped.copy()
    pop_pop_reshaped2 = pop_pop_reshaped[pop_pop_reshaped['County name'] != st]
    pop_pop_reshaped2
    # Merge with total state popluation dataframe
    pop_pop_merged = pop_pop_reshaped2.merge(pop_total, left_on = ['Year'], right_on = ['Year'])
    pop_pop_merged = pop_pop_merged.rename(columns = {'FIPS_x':'FIPS','County name_y':'State',
    'County name_x':'County Name'})
    pop_pop_merged.columns
    pop_pop_merged = pop_pop_merged.drop(columns = ['FIPS_y'])
    pop_pop_merged['State Abbreviation'] = state_abbrev
    # Remove 'county' from County and make uppercase for future merge with ARCOS data
    pop_pop_merged['County Name'] = pop_pop_merged['County Name'].str.replace(' County','').str.upper()
    pop_pop_merged

    ## Done with the function that cleans population datasets.
    ## The following code deals with mortality datasets.
    mort = pd.read_csv("20_intermediate_files/mortality_aggregate.csv")
    mort.head(20)
    # Drop columns
    mort = mort.drop(columns = ["Unnamed: 0","Notes","Year Code"])
    # Remove all rows with missing death values
    mort = mort[mort['Deaths'] != 'Missing']

    # Subset for counties that have the FIPS code from pop data
    mort_pop = mort.copy()
    # FIPS list
    pop_fips = pop.FIPS
    # Find counties in FIPS list
    mort_pop = mort_pop[mort_pop['County Code'].isin(pop_fips)]
    # Look at number of unique counties
    mort_pop['County'].nunique()
    len(mort_pop)

    # Look at drug cause codes (all with D)
    drug_overdose_codes = ['D1','D2','D4']
    mort_pop_drug = mort_pop.copy()
    mort_pop_drug = mort_pop_drug[mort_pop_drug['Drug/Alcohol Induced Cause Code'].isin(drug_overdose_codes)]

    # Convert column types
    mort_pop_drug['Deaths'] = mort_pop_drug['Deaths'].astype(float).astype(int)
    mort_pop_drug['County Code'] = mort_pop_drug['County Code'].astype(int)
    mort_pop_drug['Year'] = mort_pop_drug['Year'].astype(int)

    # Merge with population data on FIPS
    merged_data = pop_pop_merged.merge(mort_pop_drug, how = "outer", left_on = ['FIPS', 'Year'],
    right_on = ['County Code', 'Year'])
    # Check and remove extraneous columns
    merged_data
    merged_data = merged_data.drop(columns = ['County','County Code'])
    # Rename and reorder columns
    merged_data = merged_data.rename(columns = {'County_y':'County','Population':'County Population'})
    merged_data['State Abbreviation'] = state_abbrev
    merged_data.head()
    merged_data = merged_data[['County Name','State','State Abbreviation','FIPS','Year','Drug/Alcohol Induced Cause',
    'Drug/Alcohol Induced Cause Code','Deaths','County Population','State Population']]
    # Remove all years before 2003 and after 2015
    merged_data = merged_data[(merged_data['Year'] >= 2003) & (merged_data['Year'] <= 2015)]

    # Fill all NAs in death column to 0s
    merged_data['Deaths'] = merged_data['Deaths'].fillna(0).astype(int)
    # Final merged dataset
    merged_data
    return(merged_data)

# Return final merged table and save to csv
pop_mort_data = pop_mort_merge(state)
pop_mort_data
# View a sample of the data to confirm
pop_mort_data.sample(50)


# Save population data to csv
pop_mort_data.to_csv("20_intermediate_files/{}MortPopData.csv".format(state_abbrev), index = False)
