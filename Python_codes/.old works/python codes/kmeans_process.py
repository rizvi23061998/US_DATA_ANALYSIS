import numpy as np
import pandas as pd
 
path = "../US-Data-Edited/"

kmeans_df = pd.read_csv(path+'kmeans_result.csv', index_col=0)

covid_df = pd.read_csv(path+'covid_usa_edited.csv').merge(kmeans_df[['FIPS', 'Cluster_No']], on='FIPS')

mean_df = covid_df.drop(columns=['FIPS', 'STATE_FIPS']).groupby(['Cluster_No']).mean()
mean_df = mean_df.reset_index().melt(id_vars=['Cluster_No'], var_name='features', value_name='mean')

cv_df = kmeans_df.drop(columns=['FIPS', 'STATE_FIPS']).groupby(['Cluster_No']).aggregate(lambda x: x.std() / x.mean())
cv_df = cv_df.reset_index().melt(id_vars=['Cluster_No'], var_name='features', value_name='cv')

description_df = pd.merge(mean_df, cv_df, on=['Cluster_No', 'features'])

description_df.to_csv(path+'kmeans_description.csv', index=False)