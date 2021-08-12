import numpy as np
import pandas as pd
from scipy import stats

path = "../US-Data-Edited/"

df = pd.read_csv(path+"aggregate-county_all.csv")
df2 = pd.read_csv(path+"covid_usa.csv")

demographic_cols = ['POP13_SQMI', 'WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
       'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
       'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
       'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
       'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'AVE_HH_SZ', 'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD',
       'MARHH_NO_C', 'MHH_CHILD', 'FHH_CHILD', 'FAMILIES', 'AVE_FAM_SZ',
       'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC']
comorbidities_cols = ['Prevalence of obesity','Hypertension', 'Diabetes','CVD','HIV/AIDS']
climate_cols = ['IECC Climate Zone', 'IECC Moisture Regime','BA Climate Zone']
index_cols = ['FIPS', 'STATE_FIPS']
covid_cols = ['population','covid_cases','covid_deaths']

cols_to_normalize = ['WHITE', 'BLACK', 'AMERI_ES', 'ASIAN',
       'HAWN_PI', 'HISPANIC', 'OTHER', 'MULT_RACE', 'MALES', 'FEMALES',
       'AGE_UNDER5', 'AGE_5_9', 'AGE_10_14', 'AGE_15_19', 'AGE_20_24',
       'AGE_25_34', 'AGE_35_44', 'AGE_45_54', 'AGE_55_64', 'AGE_65_74',
       'AGE_75_84', 'AGE_85_UP','HOUSEHOLDS', 'HSEHLD_1_M', 'HSEHLD_1_F', 'MARHH_CHD',
       'MARHH_NO_C', 'MHH_CHILD', 'FHH_CHILD', 'FAMILIES',
       'HSE_UNITS', 'VACANT', 'OWNER_OCC', 'RENTER_OCC']+comorbidities_cols+covid_cols[1:]

cols_for_analysis = index_cols + covid_cols + demographic_cols
cols_to_replace_missing = demographic_cols+comorbidities_cols

merged_df = df.merge(df2,on=index_cols)
merged_df.reset_index(inplace=True,drop=True)


for each_col in cols_to_replace_missing: 
    merged_df.loc[merged_df[each_col]<0,each_col] = np.nan
    

# print('khkhh=============================================')


merged_df.loc[:,cols_to_normalize]=merged_df[cols_to_normalize].div(merged_df['population'],axis=0)

merged_df.fillna(merged_df.median(),inplace=True)

# demographic_cols+comorbidities_cols+climate_cols
# np.size(df[index_cols[0]].unique())

import matplotlib.pyplot as plt
from scipy.stats import spearmanr

cols_for_analysis = comorbidities_cols + demographic_cols
state_case_spearman = []
for name, group in merged_df.groupby('STATE_FIPS'):
  spearman_results_case = []
  for col in cols_for_analysis:
    rho, p_val = spearmanr(group[col],group[covid_cols[2]])
    if abs(rho) > 0.3 and p_val < 0.05:
      spearman_results_case.append((col,rho,p_val))
  spearman_results_case.sort(reverse=True,key=lambda x: abs(x[1]))
  for row in spearman_results_case:
    state_case_spearman.append([name]+list(row))
  # features_case = list(zip(*spearman_results_case))[0] if spearman_results_case else ()
  # print(name, features_case)

state_case_spearman_df = pd.DataFrame(state_case_spearman, columns=['STATE_FIPS','Features','Spearman_coefficient','P-value'])
# spearman_results_case_df = pd.DataFrame(spearman_results_case,columns = ["Feature","Spearman_coefficient","P-value"])

state_case_spearman_df

max_case_states = df[['STATE_FIPS','covid_deaths']].groupby('STATE_FIPS').agg('sum').sort_values('covid_deaths',ascending=False).index[:5].to_numpy()

state_case_spearman_df[state_case_spearman_df['STATE_FIPS'].isin(max_case_states)].to_csv(path+'top_5_states_deaths.csv',index=False)

spearman_results_case_df