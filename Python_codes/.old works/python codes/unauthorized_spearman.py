import numpy as np
import pandas as pd
from scipy import stats

path = "../US-Data-Edited/"

unauth_df = pd.read_csv(path+'county_unauthorized.csv')

agg_df = pd.read_csv(path+'aggregate-county_all.csv')

merged_df = agg_df.merge(unauth_df,left_on='FIPS',right_on='countyFIPS')[agg_df.columns.tolist() + ['Total Unauthorized Population']]

cols_to_normalize = ['covid_cases', 'covid_deaths', 'Total Unauthorized Population']
for column in cols_to_normalize:
  merged_df.loc[:,column] = merged_df[column] / merged_df['population']

# merged_df

# stats.spearmanr(merged_df['Total Unauthorized Population'], merged_df['covid_deaths'])

unauth_spearman = [[column]+list(stats.spearmanr(merged_df['Total Unauthorized Population'], merged_df[column])) for column in ['covid_cases','covid_deaths']]

unauth_spearman_df = pd.DataFrame(unauth_spearman, columns=['Feature','Spearman_cefficient','P-value'])

unauth_spearman_df.to_csv(path+'spearman_unauthorized.csv',index=False)