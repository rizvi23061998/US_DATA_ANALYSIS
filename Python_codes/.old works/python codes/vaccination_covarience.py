import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

covid_df = pd.read_csv(path+'covid_usa_state.csv',index_col='STATE_FIPS')
vac_df = pd.read_csv(path+'us_state_vaccinations_edited.csv')

vac_df = vac_df[['fips','people_vaccinated']].groupby('fips').last()

merged_df = covid_df.join(vac_df)

merged_df.loc[:, 'people_vaccinated'] = merged_df['people_vaccinated'].div(merged_df['population'], axis=0)

merged_df.to_csv(path+'covid&vaccination_usa_state.csv')

corr_df = merged_df.corr()

corr_df.to_csv(path+'cov_matrix_vaccination.csv')

srt_df = pd.DataFrame(corr_df.stack()).sort_values(0, ascending = False, key=lambda col: col.abs())

srt_df.to_csv(path+'cov_sorted_vaccination.csv')