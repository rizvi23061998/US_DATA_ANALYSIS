import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

from scipy import stats

def spearmanr(a, b):
  indices = a.nonzero()[0]
  if indices.shape == (0,):
    return np.nan, np.nan
  else:
    lcut = indices[0]
    rcut = indices[-1]+1
    return stats.spearmanr(a[lcut:rcut], b[lcut:rcut])

ts_df = pd.read_csv(path+'time_series-county_all.csv')

df = ts_df.pivot(index="countyFIPS", columns="Date", values=["Mean T",	"Min T",	"Max T",	"Total Precipitation",	"Relative Humidity",	"COVID Confirmed",	"COVID Deaths"])

sp = np.vectorize(spearmanr, signature='(n),(n)->(),()')

cor, p_val = sp([[df["COVID Confirmed"]], [df["COVID Deaths"]]], [df["Mean T"],	df["Min T"],	df["Max T"],	df["Total Precipitation"],	df["Relative Humidity"]])

index = df.index
columns = pd.MultiIndex.from_product([["Mean T",	"Min T",	"Max T",	"Total Precipitation",	"Relative Humidity"], ['correlation', 'pvalue']],
                                     names=['subject', 'spearman'])

files = [path+"spearman-confirmed-time_series.csv", path+"spearman-deaths-time_series.csv"]
for i in range(2):
  data = np.dstack((cor[i].T,p_val[i].T)).ravel().reshape((3141,-1))
  df = pd.DataFrame(data, index=index, columns=columns)
  df.to_csv(files[i])