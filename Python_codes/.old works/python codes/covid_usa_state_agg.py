import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

covid_df = pd.read_csv(path+'covid_usa.csv')
agg_df = pd.read_csv(path+'aggregate-county_all.csv')

demographic_cols = ['POP13_SQMI', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
       'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
       'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
       'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
       'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'AVE_HH_SZ', 'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD',
       'MARHH_NO_C', 'MHH_CHILD', 'FHH_CHILD', 'FAMILIES', 'AVE_FAM_SZ',
       'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC']
comorbidities_cols = ['Prevalence of obesity','Hypertension', 'Diabetes','CVD','HIV/AIDS']
index_cols = ['FIPS', 'STATE_FIPS']
covid_cols = ['population','covid_cases','covid_deaths']
pop_cols = ['WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
       'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
       'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
       'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
       'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD',
       'MARHH_NO_C', 'MHH_CHILD', 'FHH_CHILD', 'FAMILIES',
       'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC']+comorbidities_cols+covid_cols[1:]
avg_cols = ['POP13_SQMI','AVE_HH_SZ','AVE_FAM_SZ']

merged_df = pd.merge(agg_df, covid_df[index_cols + demographic_cols + comorbidities_cols], on=index_cols)

df = merged_df.loc[:, demographic_cols + comorbidities_cols]
df[df < 0] = np.nan
merged_df.update(df)

population = merged_df['population']
merged_df.loc[:,pop_cols] = merged_df[pop_cols].div(population, axis=0)\
                                               .fillna(merged_df.median())\
                                               .mul(population, axis=0)

pop_df = merged_df[['STATE_FIPS','population']+pop_cols].groupby('STATE_FIPS').sum()
pop_df.loc[:,pop_cols] = pop_df[pop_cols].div(pop_df['population'], axis=0)

avg_df = merged_df[['STATE_FIPS']+avg_cols].groupby('STATE_FIPS').mean()

out_df = pd.concat([pop_df,avg_df], axis=1)

out_df = out_df[covid_cols + demographic_cols + comorbidities_cols]

out_df.to_csv(path+'covid_usa_state.csv')