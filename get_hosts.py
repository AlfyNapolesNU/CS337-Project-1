import pandas as pd
import re
from functools import partial
from ourtypes.category import Category
from ourtypes.award import Award
import pickle 
import numpy
with open("common_words_hosts.pickle", "rb") as pckl:   
    common_words_host_list = pickle.load(pckl)

def remove_common_words(text, word_list):
    #negative positive golden globes
    words = [word for word in text.split(" ") if word not in word_list]
    return " ".join(words)

def remove_rt(text):
    text = text.split(" ")
    
    if "rt" in text:
        i = text.index("rt")
        return remove_rt(" ".join(text[0:i]) + " " + " ".join(text[i+2:]))
    return " ".join(text)

def hosts_helper(text, host_funcs, cohost_funcs, single_cohost_funcs, hosts):
    #check for cohosts first
    for func in cohost_funcs:
        m = func.search(text)
        if m is not None:
            name1 = remove_common_words(m["name1"], common_words_host_list)
            name2 = remove_common_words(m["name2"], common_words_host_list)
            hosts.vote_contender(name1, cocontender=name2)
            hosts.vote_contender(name2, cocontender=name1)
            return name1, name2
    #check for hosts
    for func in host_funcs:
        m = func.search(text)
        if m is not None:
            name = remove_common_words(m["name"], common_words_host_list)
            hosts.vote_contender(name)
            return name
    for func in single_cohost_funcs:
        m = func.search(text)
        if m is not None:
            name = remove_common_words(m["name"], common_words_host_list)
            hosts.vote_contender(name)
            return name
    return None
def get_hosts(tweets):
    hosts = Category(type="hosts") #our host storage object
    host_tweets = tweets[tweets["text"].str.contains("host")] #get tweets with the word host in it
    #del host_tweets["timestamp"] #we don't need this 
    host_tweets = host_tweets.map(remove_rt) #get rid of retweets
    #handle single names or no spaces?
    host_patterns = ['host (?P<name>[a-z]+ [a-z]+)', '(?P<name>[a-z]+ [a-z]+) (hosting|is hosting|will host|hosts|hosted)']
    cohost_patterns = ['(co-?|)hosts (?P<name1>[a-z]+ [a-z]+)( and | )(?P<name2>[a-z]+ [a-z]+)',
                    '(?P<name1>[a-z]+ [a-z]+)( and | )(?P<name2>[a-z]+ [a-z]+) (are (co-?|)hosting|will (co-?|)host|(co-?|)host|(co-?|)hosting|hosted)[^s]']
    single_cohost_patterns = ['cohost (?P<name>[a-z]+ [a-z]+)',
                    '(?P<name>[a-z]+ [a-z]+) (is cohosting|will cohost|cohosts|cohosting|cohosted)[^s]']
    #compile regex functions
    host_funcs = [re.compile(pat) for pat in host_patterns]
    cohost_funcs = [re.compile(pat) for pat in cohost_patterns]
    single_cohost_funcs = [re.compile(pat) for pat in single_cohost_patterns]

    #apply helper function 
    host_tweets = host_tweets.map(partial(hosts_helper, host_funcs=host_funcs, cohost_funcs=cohost_funcs, single_cohost_funcs=single_cohost_funcs, hosts=hosts))
    del host_tweets
    return hosts

def get_all_hosts(tweets):
    tweets = tweets[tweets["is_english"]] #only keep english tweets
    del tweets["is_english"] #get rid of this row
    tweets = tweets.dropna(subset=["text"])
    del tweets["timestamp"]
    h = get_hosts(tweets)
    vc = h.total_votes()
    top = vc[0]
    if top[2] is not None:
        cohost = top[2]
        if len(vc) > 10:
            possible_cohosts = [ele[0] for ele in vc]
        else:
            possible_cohosts = [ele[0] for ele in vc]
        for ch in possible_cohosts:
            if ch.replace(" ", "") == cohost:
                return str(top[0]), str(ch)


