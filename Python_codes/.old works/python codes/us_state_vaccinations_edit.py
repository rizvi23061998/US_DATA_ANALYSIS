import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

vac_df = pd.read_csv(path+"us_state_vaccinations.csv")

fips_df = pd.read_csv(path+"us-state-ansi-fips.csv")

vac_df.loc[vac_df.location == 'New York State', 'location'] = 'New York'

merged_df = vac_df.merge(fips_df, left_on='location', right_on='stname')

out_df = merged_df.drop(columns=['location','stname','stusps'])\
                  .rename(columns={'st': 'fips'})\
                  [['date', 'fips'] + vac_df.columns.tolist()[2:]]

out_df.to_csv(path+"us_state_vaccinations_edited.csv", index=False)