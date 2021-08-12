import numpy as np
import pandas as pd
from scipy import stats


def spearmanr(a, b):
  index = a.astype(bool)
  if index.all():
    return np.nan, np.nan
  else:
    return stats.spearmanr(a[index], b[index])

spearmanr = np.vectorize(spearmanr, signature='(n),(n)->(),()')


def analyze_spearman(sdc_src, covid_src, dst, date=slice(None)):
    county_col = 'countyFIPS'
    pop_col = 'population'

    sdc_df = pd.read_csv(sdc_src, index_col=county_col)\
               .drop(columns="StateFIPS")
    covid_feature = pd.read_csv(covid_src, index_col=county_col)\
                      .drop(index=0, columns=["County Name", "State", "StateFIPS"])\
                      .loc[:,date]\
                      .sum(axis=1)

    sdc_df, covid_feature = sdc_df.align(covid_feature, axis=0, join='inner')
    population = sdc_df[pop_col]
    covid_feature = covid_feature.div(population)

    cor, p_val = spearmanr(covid_feature, sdc_df.values.T)
    sp_df = pd.DataFrame({"feature": sdc_df.columns,
                          "spearman_coefficient": cor,
                          "p_value": p_val}).set_index("feature")
    sp_df.to_csv(dst)