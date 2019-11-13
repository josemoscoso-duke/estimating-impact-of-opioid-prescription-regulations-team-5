# Import libraries
import pandas as pd
import numpy as np
from plotnine import *

#Get a general sense of the Florida data.
fl = pd.read_csv('FLMortPopData.csv')
fl.head()

fl['Year'].value_counts()
# Since the policy became effective in Florida in 2010, we choose data from 2005-2009 and data from 2010-2015.
# Create two separate dataframes containing only data before and after the policcy year.
bef = range(2005, 2010)
aft = range(2010, 2016)
before_policy = fl[fl['Year'].isin(bef)]
after_policy = fl[fl['Year'].isin(aft)]
before_policy['Year'].value_counts()
after_policy['Year'].value_counts()

# For each individual year, sum up the total deaths of all the counties.
before_policy_aggr = before_policy.groupby('Year', as_index = False).sum()
# Add a column of death to state population ration for plotting purposes.
# I change the ratio to deaths per million people, to make it more obvious.
before_policy_aggr['Ratio'] = before_policy_aggr['Deaths'] * 1000000 / before_policy_aggr['State Population']

before_policy_aggr.head()
after_policy_aggr = after_policy.groupby('Year', as_index = False).sum()
# Add a column of death to state population ration for plotting purposes.
# To make the trend more obvious, multiply the ratio by one million.
after_policy_aggr['Ratio'] = after_policy_aggr['Deaths'] * 1000000 / after_policy_aggr['State Population']
after_policy_aggr


fl_plot = (ggplot() +
    geom_point(before_policy_aggr, aes(x='Year', y='Ratio')) +
    geom_point(after_policy_aggr, aes(x='Year', y = 'Ratio')) +
    geom_smooth(before_policy_aggr, aes(x='Year', y='Ratio'), method = 'lm', level = 0) +
    geom_smooth(after_policy_aggr, aes(x='Year', y='Ratio'), method = 'lm', level = 0) +
    scale_x_continuous(breaks = range(2005, 2016)) +
    ggtitle("Florida Overdose death per million capita") +
    geom_vline(xintercept=2010, colour="red"))
print(fl_plot)
fl_plot.save("fl_Mort_Pop.png")


#Get a general sense of the Washington data.

wa = pd.read_csv('WAMortPopData.csv')
wa.head()

wa['Year'].value_counts()
# Since the policy became effective in Washington in 2012, we choose data from 2007-2011 and data from 2012-2015.
# Create two separate dataframes containing only data before and after the policcy year.
wa_bef = range(2007, 2012)
wa_aft = range(2012, 2016)
wa_before_policy = wa[wa['Year'].isin(wa_bef)]
wa_after_policy = wa[wa['Year'].isin(wa_aft)]
wa_before_policy['Year'].value_counts()
wa_after_policy['Year'].value_counts()

# For each individual year, sum up the total deaths of all the counties.
wa_before_policy_aggr = wa_before_policy.groupby('Year', as_index = False).sum()
# Add a column of death to state population ration for plotting purposes.
# I change the ratio to deaths per million people, to make it more obvious.
wa_before_policy_aggr['Ratio'] = wa_before_policy_aggr['Deaths'] * 1000000 / wa_before_policy_aggr['State Population']

wa_before_policy_aggr.head()
wa_after_policy_aggr = wa_after_policy.groupby('Year', as_index = False).sum()
# Add a column of death to state population ration for plotting purposes.
wa_after_policy_aggr['Ratio'] = wa_after_policy_aggr['Deaths'] * 1000000 / wa_after_policy_aggr['State Population']
wa_after_policy_aggr



wa_plot = (ggplot() +
    geom_point(wa_before_policy_aggr, aes(x='Year', y='Ratio')) +
    geom_point(wa_after_policy_aggr, aes(x='Year', y = 'Ratio')) +
    geom_smooth(wa_before_policy_aggr, aes(x='Year', y='Ratio'), method = 'lm', level = 0) +
    geom_smooth(wa_after_policy_aggr, aes(x='Year', y='Ratio'), method = 'lm', level = 0) +
    scale_x_continuous(breaks = range(2007, 2018)) +
    ggtitle("Washington Overdose death per million capita") +
    geom_vline(xintercept=2012, colour="red"))
print(wa_plot)
wa_plot.save("wa_Mort_Pop.png")



#Get a general sense of the Texas data.

tx = pd.read_csv('TXMortPopData.csv')
tx.head()

tx['Year'].value_counts()
# Since the policy became effective in Texas in 2007, we choose data from 2003-2006 and data from 2007-2011.
# Create two separate dataframes containing only data before and after the policcy year.
tx_bef = range(2003, 2007)
tx_aft = range(2007, 2012)
tx_before_policy = tx[tx['Year'].isin(tx_bef)]
tx_after_policy = tx[tx['Year'].isin(tx_aft)]
tx_before_policy['Year'].value_counts()
tx_after_policy['Year'].value_counts()

# For each individual year, sum up the total deaths of all the counties.
tx_before_policy_aggr = tx_before_policy.groupby('Year', as_index = False).sum()
# Add a column of death to state population ration for plotting purposes.
# I change the ratio to deaths per million people, to make it more obvious.
tx_before_policy_aggr['Ratio'] = tx_before_policy_aggr['Deaths'] * 1000000 / tx_before_policy_aggr['State Population']

tx_before_policy_aggr.head()
tx_after_policy_aggr = tx_after_policy.groupby('Year', as_index = False).sum()
# Add a column of death to state population ration for plotting purposes.
tx_after_policy_aggr['Ratio'] = tx_after_policy_aggr['Deaths'] * 1000000 / tx_after_policy_aggr['State Population']
tx_after_policy_aggr



tx_plot = (ggplot() +
    geom_point(tx_before_policy_aggr, aes(x='Year', y='Ratio')) +
    geom_point(tx_after_policy_aggr, aes(x='Year', y = 'Ratio')) +
    geom_smooth(tx_before_policy_aggr, aes(x='Year', y='Ratio'), method = 'lm', level = 0) +
    geom_smooth(tx_after_policy_aggr, aes(x='Year', y='Ratio'), method = 'lm', level = 0) +
    scale_x_continuous(breaks = range(2003, 2012)) +
    ggtitle("Texas Overdose death per million capita") +
    geom_vline(xintercept=2007, colour="red") )
print(tx_plot)
tx_plot.save("tx_Mort_Pop.png")
