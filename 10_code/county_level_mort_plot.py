import pandas as pd
import numpy as np
import os
from plotnine import *

os.chdir('/Users/jianfeibi/Desktop')

#state = 'Texas'
#state_abbreeviation = 'TX'
#policy_year = 2007

def county_level_plot(state, state_abbreeviation, policy_year):
    # mort_pop = pd.read_csv('{}MortPopData.csv'.format(state_abbreeviation))
    control_state = pd.read_csv('{}ControlStateData.csv'.format(state_abbreeviation))
    #mort_pop.sample(5)
    start_year = control_state['Year'].min()
    end_year = control_state['Year'].max()

    bef = range(max(start_year, policy_year - 4), policy_year)
    aft = range(policy_year, min(end_year, policy_year + 4))
    # mort_pop_bef_policy = mort_pop[mort_pop['Year'].isin(bef)]
    control_state_bef_policy = control_state[control_state['Year'].isin(bef)]
    # mort_pop_aft_policy = mort_pop[mort_pop['Year'].isin(aft)]
    control_state_aft_policy = control_state[control_state['Year'].isin(aft)]

    # Add death per capita column to the dataset.
    # mort_pop_bef_policy['Ratio_Per_TenThousand'] = mort_pop_bef_policy['Deaths'] * 10000 / mort_pop_bef_policy['County Population']
    control_state_bef_policy['Ratio_Per_TenThousand'] = control_state_bef_policy['Deaths'] * 10000 / control_state_bef_policy['County Population']
    #mort_pop_bef_policy.sample(20)
    # mort_pop_aft_policy['Ratio_Per_TenThousand'] = mort_pop_aft_policy['Deaths'] * 10000 / mort_pop_aft_policy['County Population']
    control_state_aft_policy['Ratio_Per_TenThousand'] = control_state_aft_policy['Deaths'] * 10000 / control_state_aft_policy['County Population']
    #mort_pop_aft_policy.sample(20)

    mort_pop_plot = (ggplot() +
        geom_smooth(control_state_bef_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand', color = 'Policy State'), method = 'lm', level = 0.95) +
        geom_smooth(control_state_aft_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand', color = 'Policy State'), method = 'lm', level = 0.95) +
        scale_x_continuous(breaks = range(max(start_year, policy_year - 4), min(end_year, policy_year + 4))) +
        ggtitle("Overdose Deaths in {} per TenThousand Capita".format(state)) +
        geom_vline(xintercept = policy_year, color = 'red')
    )

    # mort_pop_plot = (ggplot() +
    #     # geom_point(mort_pop_bef_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand')) +
    #     # geom_point(mort_pop_aft_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand')) +
    #     geom_smooth(mort_pop_bef_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand', color = "color1"), method = 'lm', level = 0.95) +
    #     geom_smooth(control_state_bef_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand', color = "color2"), method = 'lm', level = 0.95) +
    #     geom_smooth(mort_pop_aft_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand', color = "color1"), method = 'lm', level = 0.95) +
    #     geom_smooth(control_state_aft_policy, aes(x = 'Year', y = 'Ratio_Per_TenThousand', color = "color2"), method = 'lm', level = 0.95) +
    #     scale_x_continuous(breaks = range(max(start_year, policy_year - 4), min(end_year, policy_year + 4))) +
    #     ggtitle("Overdose Deaths in {} per TenThousand Capita".format(state)) +
    #     scale_color_manual(name = "State", values = C(color1 = "blue", color2 = 'green')) +
    #     geom_vline(xintercept = policy_year, color = 'red')
    # )
    print(mort_pop_plot)
    mort_pop_plot.save("{}_Mort_Pop.png".format(state_abbreeviation))

county_level_plot('Texas', 'TX', 2007)
county_level_plot('Washington', 'WA', 2012)
county_level_plot('Florida', 'FL', 2010)
