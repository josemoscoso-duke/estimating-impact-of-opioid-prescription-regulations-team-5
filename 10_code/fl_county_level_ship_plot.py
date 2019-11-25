import pandas as pd
import numpy as np
import os
from plotnine import *

os.chdir('/Users/jianfeibi/Documents/duke/IDS690/estimating-impact-of-opioid-prescription-regulations-team-5')

policy_year = 2010
state = 'Florida'
state_abbrev = 'FL'

# First, conccatenate florida and its comparison states to one single dataframe.
fl = pd.read_csv('FLOpioidData.csv')
comparison = pd.read_csv('FLComparisonOpioidData.csv')
fl.head()
comparison.head()

fl_comparison = pd.concat([fl,comparison])
fl_comparison.sample(20)
fl_comparison['State Abbreviation'].value_counts()

# Add a column 'Policy State' to indicate whether the row is the policy state or not.
fl_comparison['Policy State'] = np.where(fl_comparison['State Abbreviation'] == state_abbrev, 'True', 'False')
fl_comparison.head()

# Define x-axis
start_year = fl_comparison['Year'].min()
end_year = fl_comparison['Year'].max()
bef = range(max(start_year, policy_year - 4), policy_year)
aft = range(policy_year, min(end_year, policy_year + 4))
fl_comparison_bef_policy = fl_comparison[fl_comparison['Year'].isin(bef)]
fl_comparison_aft_policy = fl_comparison[fl_comparison['Year'].isin(aft)]

fl_comparison_bef_policy['Ratio_Per_Thousand'] = fl_comparison_bef_policy['BUYER_MME'] * 1000 / fl_comparison_bef_policy['County Population']
#mort_pop_bef_policy.sample(20)
# mort_pop_aft_policy['Ratio_Per_TenThousand'] = mort_pop_aft_policy['Deaths'] * 10000 / mort_pop_aft_policy['County Population']
fl_comparison_aft_policy['Ratio_Per_Thousand'] = fl_comparison_aft_policy['BUYER_MME'] * 1000 / fl_comparison_aft_policy['County Population']

fl_shipment_plot = (ggplot() +
    geom_smooth(fl_comparison_bef_policy, aes(x = 'Year', y = 'Ratio_Per_Thousand', color = 'Policy State'), method = 'lm', level = 0.95) +
    geom_smooth(fl_comparison_aft_policy, aes(x = 'Year', y = 'Ratio_Per_Thousand', color = 'Policy State'), method = 'lm', level = 0.95) +
    scale_x_continuous(breaks = range(max(start_year, policy_year - 4), min(end_year, policy_year + 4))) +
    ggtitle("BUYER_MME in {} per Thousand Capita".format(state)) +
    geom_vline(xintercept = policy_year, color = 'red')
    )

print(fl_shipment_plot)
fl_shipment_plot.save("{}_Ship_Pop.png".format(state_abbrev))



# "{}_Ship_Pop.png".format(state_abbrev)
