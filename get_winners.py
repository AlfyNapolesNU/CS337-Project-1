import pandas as pd
import re
from functools import partial
from ourtypes.category import Category
from ourtypes.award import Award
import pickle 
import numpy
from rank_bm25 import BM25Okapi
import spacy

def remove_rt(text):
    text = text.split(" ")
    
    if "rt" in text:
        i = text.index("rt")
        return remove_rt(" ".join(text[0:i]) + " " + " ".join(text[i+2:]))
    return " ".join(text)


def format_awards(awards): 
    results = {}
    person_patterns = "actor|cecil|actress|direction|director|choreo|perfomance"
    thing_patterns = "series|mini-series|movie|film|music|comedy|song|score|motion picture"
    person_func = re.compile(person_patterns)
    thing_func = re.compile(thing_patterns)
    for award in awards:
        m = person_func.search(award)
        if m is not None:
            results[award] = Award(award, winner_type="Person")
            continue
        m = thing_func.search(award)
        if m is not None:
            results[award] = Award(award, winner_type="Thing")
        else:
            results[award] = Award(award)
    return results
        
def award_aliases(key, val):
    key = key.replace(".", "")
    aliases = [key]
    if "performance by an" in key:
        aliases += list(map(lambda x: x.replace("performance by an", ""), aliases))
    if "foreign language" in key:
        aliases += list(map(lambda x: x.replace("foreign language", "foreign"), aliases))
    if "television series" in key:
        aliases += list(map(lambda x: x.replace("television series", "tv"), aliases))
    if "television" in key:
        aliases += list(map(lambda x: x.replace("television", "tv"), aliases))
    if "motion picture" in key:
        aliases += list(map(lambda x: x.replace("motion picture", "movie"), aliases))
    if "feature" in key:
        aliases += list(map(lambda x: x.replace("feature", ""), aliases))
    if "original" in key:
        aliases += list(map(lambda x: x.replace("original", ""), aliases))
    if "series, mini-series or motion picture made for television" in key:
        aliases += list(map(lambda x: x.replace("series, mini-series or motion picture made for television", "television series"), aliases))
        #in a series mini-series or tv movie
        aliases += list(map(lambda x: x.replace("series, mini-series or motion picture made for television", "series mini-series or tv movie"), aliases))
    if "actor in a supporting role" in key:
        aliases += list(map(lambda x: x.replace("actor in a supporting role", "supporting actor"),aliases))
    elif "actress in a supporting role" in key:
        aliases += list(map(lambda x: x.replace("actress in a supporting role", "supporting actress"), aliases))
    if "motion picture made for television" in key:
        aliases += list(map(lambda x: x.replace("motion picture made for television", "tv movie"),aliases))
    if "director" in key:
        aliases += list(map(lambda x: x[:x.find("-")], aliases))
    if "screenplay" in key:
        aliases += list(map(lambda x: x.replace("screenplay", "adapted screenplay"), aliases))
    if "score" in key:
        aliases += list(map(lambda x: x[:x.find("score") + 5], aliases))

    aliases += list(map(lambda x: x.replace("-", ""), aliases))
    aliases = list(map(lambda x: x.replace("  ", " "), aliases))
    
    val.add_alias(aliases)

def bm25_search(award_name, bm25, tweets):
    q = award_name.split(" ")
    scores = bm25.get_scores(q)
    indices = numpy.argsort(scores)
    relevant = tweets.iloc[indices]
    return relevant[-500:]

def winner_stop_words(tweet1, list2=False):
    tweet = str(tweet1)
    toreplace = ["goldenglobes", "recipient", "anclerts", "award for", "just", "goes to", "mr president", "love him", "for winning",
                 "has known", "finally", "yes", "at the", " is ", "first", " for ", "bazinga rs", "amen",
                 "no surpres", "well deserved", "no surprises", "this generation", " to ", "goldenglobe", "goldenglobes"]
    if list2: toreplace = ["golden", "live", "blog", "globes", "annual", "award for", "goldenglobes", "award", "awards"]
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
        return winner_stop_words(tweet)
    
def winner_helper(tweet, v, won_funcs):
    if v.winner_type == "Person": tweet = winner_stop_words(tweet)
    else: tweet = winner_stop_words(tweet, list2=True)
        
    for f in won_funcs:
        m = f.findall(tweet)
        if m != []:
            if isinstance(m[0], tuple):
                for ele in m[0]:
                    if v.winner_type != "Person":
                        i = ele.find("by")
                        if i != -1:
                            ele = ele[:i]
                    else:
                        if "win" in ele or "won" in ele:
                            continue

                    v.add_winner(ele)
                    if v.winner_type != "Person": break
            else:
                ele = m[0]
                if v.winner_type != "Person":
                    i = ele.find("by")
                    if i != -1:
                        ele = ele[:i]
                else:
                    if "win" in ele or "won" in ele:
                        continue
                v.add_winner(ele)
                if v.winner_type != "Person": break
    return

def extra_winner_helper(tweet, v, spacy_model):
    tweet = winner_stop_words(tweet, list2=True)
    spacy_output = spacy_model(tweet)
    for entity in spacy_output.ents:
        if entity.label_ == "PERSON":
            v.add_winner(entity.text)
    return

def get_all_winners(tweets, awards_list):
    awards = format_awards(awards_list)
    for k, v in awards.items():
        award_aliases(k,v)
    tweets = tweets.map(lambda x: remove_rt(x.lower()))
    #tweets = tweets.map(lambda x: x.lower())
    corpus = tweets.to_numpy()
    tokenized_corpus = [str(tweet).split(" ") for tweet in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    spacy_model = spacy.load("en_core_web_sm")

    for k, v in awards.items():
        award_names = v.aliases
        won_patterns = [f"{award} (?P<name>[a-z]+ ?[a-z-]+)" for award in award_names]
        won_patterns += [f"(?P<name>[a-z]+ ?[a-z-]+)( wins? | recieves | recieved | on winning | has? won | got| wins the | ){award}" for award in award_names]
        won_funcs = [re.compile(ele) for ele in won_patterns]
        #presenter_patterns = [f"(?P<name>[a-z]+ ?[a-z]+)( presents? | presenting | are presenting ){award}" for award in award_names]
        #presenter_funcs = [re.compile(ele) for ele in presenter_patterns]
        relevant = bm25_search(award_names[0], bm25, tweets)
        if v.winner_type == "Person":
            r = relevant.map(partial(winner_helper, v=v, won_funcs=won_funcs))
            if v.winners.contenders == {}:
                relevant = bm25_search(award_names[-1],  bm25, tweets)
                r = relevant.map(partial(extra_winner_helper, v=v, spacy_model=spacy_model))
        else:
            won_patterns = [f"{award} [for ]?(?P<name>[a-z ]+)" for award in award_names]
            won_patterns += [f"(?P<name>[a-z ]+)( wins? | on winning | has? won | got| wins the | ){award}" for award in award_names]
            won_funcs = [re.compile(ele) for ele in won_patterns]
            r = relevant.map(partial(winner_helper, v=v, won_funcs=won_funcs))
    return awards
