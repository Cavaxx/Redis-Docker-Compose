import pandas as pd
import dask.dataframe as dd
import dask.bag as da
import os
import json
import dask
import redis 

redis_client = redis.Redis(host= "localhost", port=6378)

from dask.distributed import LocalCluster
cluster = LocalCluster()          # Fully-featured local Dask cluster
client = cluster.get_client()

csv_df = pd.read_csv('/home/ubuntu/Data_Science/Big_Data/dask-lab/pokemonDB_dataset.csv')

parquet_df = dd.read_parquet('/home/ubuntu/Data_Science/Big_Data/dask-lab/trainers_with_pockemon.parquet')
mean_def = csv_df['Defense Max'].mean()

filter = csv_df[csv_df['Defense Max'] > mean_def]

merge_df = parquet_df.merge(filter)

merge_df = merge_df.drop(['pockemon'], axis=1)

merge_df['team_name'] = merge_df['first_name'] + merge_df['last_name']

merge_df = merge_df.drop(['first_name', 'last_name'], axis=1)

high_def_team = merge_df.groupby(['team_name']).agg({'Defense Max': 'mean'})

high_def_team.compute()


connection = redis_client

for e in connection:
    connection.set(e[0], e[1])


