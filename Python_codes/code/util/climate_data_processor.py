import numpy as np
import pandas as pd


def concat_climate_data(srcs, dst):
    dfs = [pd.read_csv(src) for src in srcs]
    df = pd.concat(dfs).sort_values(by=['FIPS', 'Date'])
    df.to_csv(dst, index=False)