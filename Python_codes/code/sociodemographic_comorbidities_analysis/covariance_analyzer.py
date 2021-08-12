import numpy as np
import pandas as pd
from itertools import combinations


def analyze_covariance_sdc(src, dst):
    sdc_df = pd.read_csv(src, index_col='countyFIPS')\
               .drop(columns="StateFIPS")
    
    cov_df = sdc_df.cov()
    data = [(f1, f2, cov_df.loc[f1, f2]) for f1, f2 in combinations(sdc_df.columns, 2)]
    srt_df = pd.DataFrame(data, columns=['feature','feature','covariance'])\
               .sort_values(by='covariance', 
                            ascending=False, 
                            key=lambda col: col.abs())
    
    srt_df.to_csv(dst, index=False)