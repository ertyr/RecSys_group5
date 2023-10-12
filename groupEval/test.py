## Make relevant imports
import numpy as np
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser
import sys

## Import relevant python files
from evalMain import groupNDCG


## Train the individual rec.sys.
# get the data
data = pd.read_csv('dataset/clean/user_ratings_neg_1000_20_20_1_train.csv', delimiter=',')
data = data.drop(columns=['Unnamed: 0'])

# construct dataframe in format (user, item, rating) via column addition
df_ui = data.rename(columns={"UserID": "user", "JobID": "item", "Rating":"rating"})
# check data being read properly

# train UserUser collaborative filterring
user_user = UserUser(10, min_nbrs=3)  # Minimum (3) and maximum (10) number of neighbors to consider
recsys = Recommender.adapt(user_user)
recsys.fit(df_ui)


## Read dataframe generated by group aggregation (groupAggregation.ipynb)
df_grpAggr = pd.read_csv('groupAgg/grpAggr.csv', delimiter=',')
df_grpAggr = df_grpAggr.drop(columns=['Unnamed: 0']) # removing useless index column

################## Not working part

## Compute ndcg for a group
grp_results = pd.DataFrame(columns=["mean","min","max"])

for i, row in df_grpAggr.iterrows():
    # convert strings to list of strings
    strMem = (row["Members"])[1:(len(row["Members"])-1)]
    strRec = (row["Recommendation"])[1:(len(row["Recommendation"])-1)]

    lstMem = strMem.split(", ")
    lstRec = strRec.split(", ")
    # convert lists of strings to int
    lstMem = list(map(int, lstMem))
    lstRec = list(map(int, lstRec))

    # run group ndcg
    g_mean, g_min, g_max = groupNDCG(lstMem, lstRec, recsys) # error inside
    grp_results.loc[len(grp_results.index)] = [g_mean, g_min, g_max] 


