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
cols_to_normalize = ['WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
       'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
       'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
       'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
       'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD',
       'MARHH_NO_C', 'MHH_CHILD', 'FHH_CHILD', 'FAMILIES',
       'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC']+comorbidities_cols+covid_cols[1:]

merged_df = pd.merge(agg_df, covid_df[index_cols + demographic_cols + comorbidities_cols], on=index_cols)

df = merged_df.loc[:, demographic_cols + comorbidities_cols]
df[df < 0] = np.nan
merged_df.update(df)

merged_df.loc[:,cols_to_normalize] = merged_df[cols_to_normalize].div(merged_df['population'], axis=0)
merged_df.fillna(merged_df.median(),inplace=True)

merged_df.to_csv(path+'covid_usa_edited.csv', index=False)