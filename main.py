from get_hosts import get_all_hosts
from get_winners import get_all_winners
from preprocessing import preproccessing
from get_awards import extract_award_names
import pandas as pd

official_awards_list = ["best performance by an actor in a television series - comedy or musical", 
          "best performance by an actor in a television series - drama",
          "best performance by an actor in a motion picture - drama",
          "best performance by an actress in a mini-series or motion picture made for television",
          "best original song - motion picture", 
          "best animated feature film",
            "best television series - comedy or musical",
          "best performance by an actor in a mini-series or motion picture made for television", 
          "best television series - drama", 
          "best performance by an actress in a supporting role in a motion picture",
          "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television", 
          "best motion picture - drama",
          "best performance by an actor in a motion picture - comedy or musical", 
          "cecil b. demille award", 
          "best performance by an actress in a motion picture - drama",
          "best performance by an actress in a television series - drama", 
          "best original score - motion picture", 
          "best mini-series or motion picture made for television",
          "best performance by an actress in a motion picture - comedy or musical", 
          "best motion picture - comedy or musical", 
          "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television",
          "best performance by an actor in a supporting role in a motion picture",
          "best foreign language film", 
          "best performance by an actress in a television series - comedy or musical",
          "best director - motion picture", "best screenplay - motion picture"]

json_file = "gg2013.json"
tweets_df = preproccessing(json_file=json_file)
    
#call to get hosts
hosts = get_all_hosts(tweets_df)
#list of hosts

#call to get awards 
award_names = extract_award_names(tweets_df)
awards = award_names[:27]

#call to get winners
winners = get_all_winners(tweets_df, official_awards_list)
assert isinstance(winners, dict)

#get nominees

#get presenters