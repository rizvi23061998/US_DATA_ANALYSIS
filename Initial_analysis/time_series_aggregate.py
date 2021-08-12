# -*- coding: utf-8 -*-
"""covid-19.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t87I7WpL5S3iRdjEeq7SQls1tp1nZZgI
"""

import numpy as np
import pandas as pd
 
path = "/content/drive/MyDrive/CSE BUET/Level-4, Term-2/CSE 400/COVID-19/US-Data-Edited/"

index = ["countyFIPS", "stateFIPS"]
columns = ["County Name","State"]
files = ['county_population.csv', 'time_series-county_covid_confirmed.csv', 'time_series-county_covid_deaths.csv']

population_df, covid_confirmed_df, covid_deaths_df = (pd.read_csv(path+f).drop(columns=columns).set_index(index) for f in files)

aggregate_confirmed_df = covid_confirmed_df.sum(axis=1).rename("COVID Confirmed").to_frame()
aggregate_deaths_df = covid_deaths_df.sum(axis=1).rename("COVID Deaths").to_frame()
df = population_df.merge(aggregate_confirmed_df, on=index).merge(aggregate_deaths_df, on=index)
df.to_csv(path+"aggregate-county_all.csv")