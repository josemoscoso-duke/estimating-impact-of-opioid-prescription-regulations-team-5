# Import libraries
import pandas as pd
import numpy as np
from plotnine import *

# BEFORE STARTING: download state population data from this link https://data.ers.usda.gov/reports.aspx?ID=17827
# and adjust the csv to have the following columns: FIPS, County name, RUC Code, Pop. 1990,
# Pop. 2000, Pop. 2010, Pop. 2018, Change 2010-2018. After downloading, you must delete the image textbox and then manually
# readjust the columns so that it is in this format. Save as "StatePopReportCleaned" and add
# 00/source/Population in Github
# See template of "popshingtonPopReportCleaned" in source files

# Input state name and abbreivation
state = 'Florida'
state_abbrev = 'FL'

# Function to clean population and mortality data and then merge the two dataframes
def pop_mort_merge(st):
    # Import state population data
    pop = pd.read_csv("../00_source/Population/{}PopulationReportCleaned.csv".format(st), sep = ',')

    # Drop extra column and recheck dataframe
    pop = pop.drop(columns = "Unnamed: 8")
    pop

    # Rename FIPS column
    pop = pop.rename(columns = {"FIPS*":"FIPS"})

    # Population estimation
    pop_pop = pop.copy()
    # Convert columns to float types (replace commas and %)
    pop_pop['Pop. 1990'] = pop_pop['Pop. 1990'].str.replace(',','').astype(int)
    pop_pop['Pop. 2000'] = pop_pop['Pop. 2000'].str.replace(',','').astype(int)
    pop_pop['Pop. 2010'] = pop_pop['Pop. 2010'].str.replace(',','').astype(int)
    pop_pop['Pop. 2018'] = pop_pop['Pop. 2018'].str.replace(',','').astype(int)
    pop_pop['Change 2010-18'] = pop_pop['Change 2010-18'].str.replace('%','').astype(float)
    pop_pop
    # Assume linear increase in population from 2000 to 2018 (find change per year)
    avg_change_10 = (pop_pop['Pop. 2010'] - pop_pop['Pop. 2000'])/10
    avg_change_18 = (pop_pop['Pop. 2018'] - pop_pop['Pop. 2010'])/9
    # Create columns of population for each year
    year_list = list(range(1,18))
    for i in year_list:
        if i < 10:
            pop_pop['Pop. 200' + str(i)] = pop_pop['Pop. 200' + str(i-1)] + avg_change_10
        elif i == 10:
            pop_pop['Pop. 20' + str(i)] = pop_pop['Pop. 200' + str(i-1)] + avg_change_10
        else:
            pop_pop['Pop. 20' + str(i)] = pop_pop['Pop. 20' + str(i-1)] + avg_change_18
    # Drop and reorder columns
    pop_pop = pop_pop.drop(columns = ["RUC code","Pop. 1990","Change 2010-18"])
    pop_pop = pop_pop[['FIPS', 'County name', 'Pop. 2000','Pop. 2001', 'Pop. 2002',
    'Pop. 2003', 'Pop. 2004', 'Pop. 2005', 'Pop. 2006', 'Pop. 2007',
    'Pop. 2008', 'Pop. 2009', 'Pop. 2010','Pop. 2011', 'Pop. 2012', 'Pop. 2013',
    'Pop. 2014', 'Pop. 2015', 'Pop. 2016','Pop. 2017', 'Pop. 2018']]
    # Rename columns to be years
    pop_pop = pop_pop.rename(columns = {"Pop. 2000":"2000", "Pop. 2001":"2001", "Pop. 2002":"2002",
    "Pop. 2003":"2003", "Pop. 2004":"2004", "Pop. 2005":"2005", "Pop. 2006":"2006", "Pop. 2007":"2007",
    "Pop. 2008":"2008", "Pop. 2009":"2009", "Pop. 2010":"2010", "Pop. 2011":"2011", "Pop. 2012":"2012",
    "Pop. 2013":"2013", "Pop. 2014":"2014", "Pop. 2015":"2015", "Pop. 2016":"2016", "Pop. 2017":"2017",
    "Pop. 2018":"2018", "Pop. 2019":"2019"})
    pop_pop

    # FIPS list
    pop_fips = pop.FIPS
    pop_fips

    # Reshape population table to have following columns: FIPS, County, Year, population
    pop_pop_reshaped = pd.melt(pop_pop, id_vars = ['FIPS','County name'],
    value_vars = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
    '2011','2012','2013','2014','2015','2016','2017','2018'], var_name = 'Year', value_name = 'Population')

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
    'County name_x':'County'})
    pop_pop_merged.columns
    pop_pop_merged = pop_pop_merged.drop(columns = ['FIPS_y'])
    pop_pop_merged

    mort = pd.read_csv("../20_intermediate_files/mortality_aggregate.csv")
    mort.head(20)
    # Drop columns
    mort = mort.drop(columns = ["Unnamed: 0","Notes"])
    # Remove all rows with missing death values
    mort = mort[mort['Deaths'] != 'Missing']

    # Subset for counties that have the FIPS code from pop data
    mort_pop = mort.copy()
    mort_pop = mort_pop[mort_pop['County Code'].isin(pop_fips)]
    # Look at number of unique counties
    mort_pop['County'].nunique()
    len(mort_pop)

    # Look at drug cause codes (all with D)
    drug_overdose_codes = ['D1','D2','D4']
    mort_pop_drug = mort_pop[mort_pop['Drug/Alcohol Induced Cause Code'].isin(drug_overdose_codes)]
    #mort_pop_drug['Deaths'].astype(float).sum()
    # Drop year code column
    mort_pop_drug = mort_pop_drug.drop(columns = "Year Code")

    # Convert column types
    mort_pop_drug['Deaths'] = mort_pop_drug['Deaths'].astype(float).astype(int)
    mort_pop_drug['County Code'] = mort_pop_drug['County Code'].astype(int)
    mort_pop_drug['Year'] = mort_pop_drug['Year'].astype(int)
    # mort_pop_drug['Drug/Alcohol Induced Cause'] = mort_pop_drug['Drug/Alcohol Induced Cause'].astype(str)
    # mort_pop_drug['Drug/Alcohol Induced Cause Code'] = mort_pop_drug['Drug/Alcohol Induced Cause Code'].astype(str)
    mort_pop_drug.dtypes

    # Merge with population data on FIPS
    merged_data = mort_pop_drug.merge(pop_pop_merged, how = "left", left_on = ['County Code', 'Year'],
    right_on = ['FIPS', 'Year'])
    # Check and remove extraneous columns
    merged_data
    merged_data = merged_data.drop(columns = ['County_x','FIPS'])
    # Rename and reorder columns
    merged_data = merged_data.rename(columns = {'County_y':'County','Population':'County Population'})
    merged_data.head()
    merged_data = merged_data[['County','State','County Code','Year','Drug/Alcohol Induced Cause',
    'Drug/Alcohol Induced Cause Code','Deaths','County Population','State Population']]
    # Final merged dataset
    merged_data
    print(merged_data['Deaths'])

    return(merged_data)

pop_mort_merge(state)
