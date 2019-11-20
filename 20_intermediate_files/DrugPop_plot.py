# Import libraries
import pandas as pd
import numpy as np
from plotnine import *
import os
# Set base directory
os.chdir("~/estimating-impact-of-opioid-prescription-regulations-team-5")
# Get a general sense of the Florida data.
fl = pd.read_csv('FLOpioidData.csv')
fl.sample(10)
fl['TRANSACTION_MONTH'].value_counts()
fl['TRANSACTION_YEAR'].value_counts()

# Create a new column filled with int value 1,
# so the sum of this column represents
# total number of transaction after aggregation.
fl['tocount'] = 1
fl.head()

# Get the total transaction numbers for each individual year.
fl_aggr = fl.groupby(['TRANSACTION_YEAR', 'State Population'], as_index=False).sum()
fl_aggr.drop(columns=['TRANSACTION_MONTH'], inplace=True)
fl_aggr

# Create a column representing drug per capita.
fl_aggr['Drug_Per_Capita'] = fl_aggr['BUYER_MME'] / fl_aggr['State Population']
fl_aggr
# To make trend more obvious, try multiply Drug_Per_Capita by 10.
fl_aggr['Drug_Per_Capita'] = fl_aggr['Drug_Per_Capita'] * 10
fl_aggr

bef = range(2006, 2010)
aft = range(2010, 2013)
before_policy = fl_aggr[fl_aggr['TRANSACTION_YEAR'].isin(bef)]
after_policy = fl_aggr[fl_aggr['TRANSACTION_YEAR'].isin(aft)]

fl_plot = (ggplot() +
    geom_line(before_policy, aes(x='TRANSACTION_YEAR', y='Drug_Per_Capita')) +
    geom_line(after_policy, aes(x='TRANSACTION_YEAR', y='Drug_Per_Capita')) +
    scale_x_continuous(breaks = range(2005, 2013)) +
    ggtitle("Florida Drug Dosage Per Capita") +
    geom_vline(xintercept=2010, colour="red"))
print(fl_plot)
fl_plot.save("fl_Drug_Pop.png")


# Get a general sense of the Washington data.
wa = pd.read_csv('WAOpioidData.csv')
wa.sample(10)
wa['TRANSACTION_MONTH'].value_counts()
wa['TRANSACTION_YEAR'].value_counts()
