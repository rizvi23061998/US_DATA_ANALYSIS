import numpy as np
import pandas as pd

path = "../US-Data-Edited/"

climate_df = pd.read_csv(path+'time_series-county_climate.csv')
covid_confirmed_df = pd.read_csv(path+'time_series-county_covid_confirmed.csv')
covid_deaths_df = pd.read_csv(path+'time_series-county_covid_deaths.csv')

columns = ["County Name",	"State",	"stateFIPS"]
covid_confirmed_df = covid_confirmed_df.drop(columns=columns)
covid_deaths_df = covid_deaths_df.drop(columns=columns)

id_vars=["countyFIPS"]
var_name = "Date"

covid_confirmed_df = covid_confirmed_df.melt(id_vars=id_vars, var_name=var_name, value_name="COVID Confirmed")
covid_deaths_df = covid_deaths_df.melt(id_vars=id_vars, var_name=var_name, value_name="COVID Deaths")

date_col = "Date"
for df in [climate_df, covid_confirmed_df, covid_deaths_df]:
  df[date_col] = pd.to_datetime(df[date_col])

keys = ["countyFIPS","Date"]
df = climate_df.merge(covid_confirmed_df, on=keys).merge(covid_deaths_df, on=keys)

df.to_csv(path+'time_series-county_all.csv',index=False)