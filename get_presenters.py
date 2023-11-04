import pandas as pd
import re
from ourtypes.category import Category
from ourtypes.award import Award

def stop_words(tweet1):
    tweet = str(tweet1)
    toreplace = ["golden", "live", "blog", "globes", "annual", "award for", "goldenglobes", "award", "awards"]
    for ele in toreplace:
        tweet = tweet.replace(ele, " ")
    
    if "http" in tweet:
        tweetList = tweet.split(" ")
        for ele in tweetList:
            if "http" in ele:
                tweetList.remove(ele)
        tweet = " ".join(tweetList)
    if tweet == tweet1:
        tweet = tweet.replace(".", "").replace(" - "," ")
        return tweet.replace("  "," ").replace("  "," ")
    else:
        return stop_words(tweet)
    

def get_presenters(tweets_df, awards):
    presenters = ["(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) and (?P<name2>[A-Z][a-z]* [A-Z][a-z-]*) presenting [for]?",
              "(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) and (?P<name2>[A-Z][a-z]* [A-Z][a-z-]*)( are| to|) present the (nominees|winners) for",
              "(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) and (?P<name2>[A-Z][a-z]* [A-Z][a-z-]*)( are| to|) present",
              "(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) and (?P<name2>[A-Z][a-z]* [A-Z][a-z-]*) introducing"
    ]

    presenter_funcs = [re.compile(ele) for ele in presenters]
    presenter = ["(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) presenting [for]?",
                "(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) presents the (nominees|winners) for",
                "(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) [to]? presents?",
                "(?P<name1>[A-Z][a-z]* [A-Z][a-z-]*) introducing"
    ]

    presenter_func = [re.compile(ele) for ele in presenters]

    possible_presenters = []
    for i, tweet in tweets_df.iterrows():
        tweet = str(tweet["text"])
        for f in presenter_funcs:
            m = f.search(tweet)
            if m is not None:
                name1 = m["name1"].lower()
                name2 = m["name2"].lower()
                span = m.span()
                award = stop_words(tweet[span[1]:].lower())
                if len(award) > 10:
                    possible_presenters.append((name1, name2, award))
        for f in presenter_func:
            m = f.search(tweet)
            if m is not None:
                name1 = m["name1"].lower()
                span = m.span()
                award = stop_words(tweet[span[1]:].lower())
                if len(award) > 5:
                    possible_presenters.append((name1, None, award))


    for award in awards.values():
        award_names = award.aliases
        for p in possible_presenters:
            for a in award_names:
                if a in p[2]:
                    if p[1] is not None:
                        award.add_presenter(p[0], p[1])
                        award.add_presenter(p[1], p[0])
                    else:
                        award.add_presenter(p[0])
    
    return awards