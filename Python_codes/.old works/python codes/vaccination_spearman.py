import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

covid_df = pd.read_csv(path+'covid&vaccination_usa_state.csv',index_col='STATE_FIPS')

vac_df = covid_df['people_vaccinated']
covid_df = covid_df.drop(columns='people_vaccinated')

from scipy.stats import spearmanr

sp = np.vectorize(spearmanr, signature='(n),(n)->(),()')
result = sp(covid_df.to_numpy().T, vac_df)

sp_df = pd.DataFrame({'spearman vs vaccination': covid_df.columns, 'correlation': result[0], 'pvalue': result[1]})

sp_df.to_csv(path+'spearman-vaccination-tabular.csv', index=False)