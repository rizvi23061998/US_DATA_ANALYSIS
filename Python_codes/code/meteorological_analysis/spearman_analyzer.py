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


def analyze_spearman(climate_src, covid_src, dst, date=slice(None)):
    fips_col = "countyFIPS"
    date_col = "Date"
    covid_col = "covid_feature"
    
    climate_df = pd.read_csv(climate_src)\
                   .rename(columns={"FIPS": fips_col})
    climate_df[date_col] = pd.to_datetime(climate_df[date_col])
    
    covid_df = pd.read_csv(covid_src)\
                 .drop(columns=["County Name", "State", "StateFIPS"])\
                 .loc[:, date]\
                 .melt(id_vars=[fips_col], var_name=date_col, value_name=covid_col)
    covid_df[date_col] = pd.to_datetime(covid_df[date_col])
    
    df = climate_df.merge(covid_df, on=[fips_col,date_col])\
                   .pivot(index=fips_col, columns=date_col)
    
    climate_cols = climate_df.columns[2:]
    cor, p_val = spearmanr(df[covid_col], [df[col] for col in climate_cols])

    data = np.stack((cor.T,p_val.T), axis=-1).reshape((cor.shape[1],-1))
    index = df.index
    columns = pd.MultiIndex.from_product([climate_cols, ['correlation', 'pvalue']],
                                     names=['subject', 'spearman'])
    df = pd.DataFrame(data, index=index, columns=columns)

    df.to_csv(dst)