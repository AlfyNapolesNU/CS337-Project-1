from get_hosts import get_all_hosts
from get_winners import get_all_winners
from preprocessing import preproccessing
from get_awards import get_all_awards
import pandas as pd


if __name__ == "main":
    #preprocess tweets 
    json_file = "gg2013.json"
    tweets_df = preproccessing(json_file=json_file)
    
    #call to get hosts
    hosts = get_all_hosts(tweets_df)
    #list of 
    
    for ele in hosts:
        print(ele)
