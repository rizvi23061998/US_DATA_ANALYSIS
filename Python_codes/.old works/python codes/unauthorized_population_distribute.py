import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

df = pd.read_csv(path+'county_unauthorized_2016_v2.csv')

pop_df = pd.read_csv(path+'aggregate-county_all.csv')

merged_df = df.merge(pop_df,left_on='countyFIPS',right_on='FIPS')

combined_states = [
 [12086,12087],
 [6053,6069],
 [8001,8014,8019,8035,8039,8047,8059,8005,8013,8123],
 [22071,22051,22075,22087],
 [35001,35061],
 [53005,53021,53071],
 [45045,45059],
 [16001,16027,16045,16073,16075,16087],
 [20173,20015,20079],
 [45019,45015,45035],
 [8041,8119],
 [34011,34033],
 [1089,1095,1083],
 [53025,53037],
 [6101,6115],
 [37179,37007],
 [48015,48321,48473,48481,48089]
]

for combined_state in combined_states:
  mask = merged_df['countyFIPS'].isin(combined_state)
  temp_df = merged_df[mask]
  merged_df.loc[mask,'Total Unauthorized Population'] = temp_df['Total Unauthorized Population']*temp_df['population']/temp_df['population'].sum()

df['Total Unauthorized Population'] = merged_df['Total Unauthorized Population']

df.to_csv(path+'county_unauthorized.csv',index=False)