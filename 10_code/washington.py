# Import libraries
import pandas as pd
import numpy as np
from plotnine import *


# Import Washington population data
wa = pd.read_csv("../00_source/Population/WashingtonPopReportCleaned.csv", sep = ',')
wa.head()

# Drop extra column and recheck dataframe
wa = wa.drop(columns = "Unnamed: 8")
wa

# Rename FIPS column
wa = wa.rename(columns = {"FIPS*":"FIPS"})

# Population interpolation
wa_pop = wa.copy()
# Convert columns to float types (replace commas and %)
wa_pop['Pop. 1990'] = wa_pop['Pop. 1990'].str.replace(',','').astype(int)
wa_pop['Pop. 2000'] = wa_pop['Pop. 2000'].str.replace(',','').astype(int)
wa_pop['Pop. 2010'] = wa_pop['Pop. 2010'].str.replace(',','').astype(int)
wa_pop['Pop. 2018'] = wa_pop['Pop. 2018'].str.replace(',','').astype(int)
wa_pop['Change 2010-18'] = wa_pop['Change 2010-18'].str.replace('%','').astype(float)
wa_pop
# Assume linear increase in population from 2000 to 2018 (find change per year)
avg_change_10 = (wa_pop['Pop. 2010'] - wa_pop['Pop. 2000'])/10
avg_change_18 = (wa_pop['Pop. 2018'] - wa_pop['Pop. 2010'])/9
# Create columns of population for each year
year_list = list(range(1,18))
for i in year_list:
    if i < 10:
        wa_pop['Pop. 200' + str(i)] = wa_pop['Pop. 200' + str(i-1)] + avg_change_10
    elif i == 10:
        wa_pop['Pop. 20' + str(i)] = wa_pop['Pop. 200' + str(i-1)] + avg_change_10
    else:
        wa_pop['Pop. 20' + str(i)] = wa_pop['Pop. 20' + str(i-1)] + avg_change_18
# Drop and reorder columns
wa_pop = wa_pop.drop(columns = ["RUC code","Pop. 1990","Change 2010-18"])
wa_pop = wa_pop[['FIPS', 'County name', 'Pop. 2000','Pop. 2001', 'Pop. 2002',
'Pop. 2003', 'Pop. 2004', 'Pop. 2005', 'Pop. 2006', 'Pop. 2007',
'Pop. 2008', 'Pop. 2009', 'Pop. 2010','Pop. 2011', 'Pop. 2012', 'Pop. 2013',
'Pop. 2014', 'Pop. 2015', 'Pop. 2016','Pop. 2017', 'Pop. 2018']]
# Rename columns to be years
wa_pop = wa_pop.rename(columns = {"Pop. 2000":"2000", "Pop. 2001":"2001", "Pop. 2002":"2002",
"Pop. 2003":"2003", "Pop. 2004":"2004", "Pop. 2005":"2005", "Pop. 2006":"2006", "Pop. 2007":"2007",
"Pop. 2008":"2008", "Pop. 2009":"2009", "Pop. 2010":"2010", "Pop. 2011":"2011", "Pop. 2012":"2012",
"Pop. 2013":"2013", "Pop. 2014":"2014", "Pop. 2015":"2015", "Pop. 2016":"2016", "Pop. 2017":"2017",
"Pop. 2018":"2018", "Pop. 2019":"2019"})
wa_pop

# FIPS list
wa_fips = wa.FIPS
wa_fips

# Reshape population table to have following columns: FIPS, County, Year, population
wa_pop_reshaped = pd.melt(wa_pop, id_vars = ['FIPS','County name'],
value_vars = ['2000','2001','2002','2003','2004','2005','2006','2007','2008','2009','2010',
'2011','2012','2013','2014','2015','2016','2017','2018'], var_name = 'Year', value_name = 'Population')

# Convert to proper types
wa_pop_reshaped['Year'] = wa_pop_reshaped['Year'].astype(int)
wa_pop_reshaped['Population'] = wa_pop_reshaped['Population'].astype(int)
wa_pop_reshaped['County name'] = wa_pop_reshaped['County name'].astype(str)
wa_pop_reshaped.dtypes
wa_pop_reshaped

# Create frame of total state population
wa_total = wa_pop_reshaped.copy()
wa_total = wa_pop_reshaped[wa_pop_reshaped['County name'] == 'Washington']
wa_total
wa_total = wa_total.rename(columns = {"Population":"State Population"})
wa_total

# Remove Washington from original reshaped dataframe
wa_pop_reshaped2 = wa_pop_reshaped.copy()
wa_pop_reshaped2 = wa_pop_reshaped[wa_pop_reshaped['County name'] != 'Washington']
wa_pop_reshaped2
# Merge with total state popluation dataframe
wa_pop_merged = wa_pop_reshaped2.merge(wa_total, left_on = ['Year'], right_on = ['Year'])
wa_pop_merged = wa_pop_merged.rename(columns = {'FIPS_x':'FIPS','County name_y':'State',
'County name_x':'County'})
wa_pop_merged.columns
wa_pop_merged = wa_pop_merged.drop(columns = ['FIPS_y'])
wa_pop_merged

# Import Mortality stats
mort = pd.read_csv("../20_intermediate_files/mortality_aggregate.csv")
mort.head(20)
# Drop columns
mort = mort.drop(columns = ["Unnamed: 0","Notes"])
# Remove all rows with missing death values
mort = mort[mort['Deaths'] != 'Missing']

# Subset for counties that have the FIPS code from WA data
mort_wa = mort.copy()
mort_wa = mort_wa[mort_wa['County Code'].isin(wa_fips)]
# Look at number of unique counties
mort_wa['County'].nunique()
len(mort_wa)

# Look at drug cause codes (all with D)
drug_overdose_codes = ['D1','D2','D4']
mort_wa_drug = mort_wa[mort_wa['Drug/Alcohol Induced Cause Code'].isin(drug_overdose_codes)]
#mort_wa_drug['Deaths'].astype(float).sum()
# Drop year code column
mort_wa_drug = mort_wa_drug.drop(columns = "Year Code")

# Convert column types
mort_wa_drug['Deaths'] = mort_wa_drug['Deaths'].astype(float).astype(int)
mort_wa_drug['County Code'] = mort_wa_drug['County Code'].astype(int)
mort_wa_drug['Year'] = mort_wa_drug['Year'].astype(int)
# mort_wa_drug['Drug/Alcohol Induced Cause'] = mort_wa_drug['Drug/Alcohol Induced Cause'].astype(str)
# mort_wa_drug['Drug/Alcohol Induced Cause Code'] = mort_wa_drug['Drug/Alcohol Induced Cause Code'].astype(str)
mort_wa_drug.dtypes

# Merge with population data on FIPS
merged_data = mort_wa_drug.merge(wa_pop_merged, how = "left", left_on = ['County Code', 'Year'],
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
merged_data['Deaths'].value_counts()
