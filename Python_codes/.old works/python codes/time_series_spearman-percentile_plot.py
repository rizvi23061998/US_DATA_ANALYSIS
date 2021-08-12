# !pip install probscale

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
# %matplotlib inline

path = "../US-Data-Edited/"

df = pd.read_csv(path+'spearman-county_covid_confirmed.csv', header=[0, 1],index_col=0)

import warnings
warnings.simplefilter('ignore')

import numpy
from matplotlib import pyplot
import seaborn

import probscale
pyplot.style.use('dark_background')

from scipy import stats

def plot_percentile(df, feature):
  sub_df = df[feature]
  sub_df = sub_df[sub_df['pvalue'] < 0.05]
  position, cor = probscale.plot_pos(sub_df['correlation'].dropna())
  position *= 100
  fig, ax = pyplot.subplots(figsize=(6, 3))
  ax.plot(position, cor, marker='.', linestyle='none', label='Bill amount')
  ax.set_xlabel('Percentile')
  ax.set_ylabel('Spearman of ' + feature)
  # ax.set_yscale('log')
  ax.set_ylim(bottom=-1, top=1)
  pyplot.show()

plot_percentile(df, 'Relative Humidity')

df.columns