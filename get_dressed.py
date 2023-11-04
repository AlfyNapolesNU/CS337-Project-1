import pandas as pd
import re
from functools import partial


def stop_words(tweet1, list2=False):
    tweet = str(tweet1)
    if list2: stop_words_list = ['of', "globes", "globe", "golden", 'the', 'so', 'far', 'yet', 'again', 'in', 'my', 'at', 'eredcarpet', 'httptco', 'post', 'on', 'list', 
                   'httptcox', 'for', 'me', 'how', 'about', 'tonight', 'goldenglobes', 'category', 'this', 'they', 'look', 
                   'too', 'tonite', 'nominee', 'idontwatchijustlurkoutfits', 'golden', 'tonights', 'from', "is", "easily", "one", 'and', 
                   'tmrw', 'tweethearts', "which", 'stars', 'people', 'person', 'due', 'to', 'hands', 'down', 'every', 'make', 
                   'up', 'woman', 'was', 'more', 'go', 'dude', 'men']
    else: stop_words_list = ['of', "globes", "globe", "golden", 'the', 'so', 'far', 'yet', 'again', 'my', 'at', 'eredcarpet', 'httptco', 'post', 'on', 'list', 
                   'httptcox', 'for', 'me', 'how', 'about', 'tonight', 'goldenglobes', 'category', 'this', 'they', 'look', 
                   'too', 'tonite', 'nominee', 'idontwatchijustlurkoutfits', 'golden', 'tonights', 'from', 
                   'tmrw', 'tweethearts', 'stars', 'people', 'person', 'due', 'to', 'hands', 'down', 'every', 'make', 
                   'up', 'woman', 'was', 'more', "which", 'go', 'dude', 'men']

    word_list = tweet.split(" ")
    for word in word_list:
        if word.lower().strip() in stop_words_list:
            word_list.remove(word)
    tweet = " ".join(word_list)
    
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
    
def dressed_helper(tweet, func, cat):
    if cat == "worst":
        tweet = stop_words(tweet, list2=True)
    else:
        tweet = stop_words(tweet)
    
    if tweet is not None:
        for f in func:
            m = f.search(tweet)
            if m is not None:
                name = m["name"]
                return name
            
def format_output(names):
    names = names.dropna().tolist()
    d = {}
    for name in names:
        name = name.lower()
        d[name] = d.get(name, 0) + 1
    d = sorted(d, reverse=True)
    return d 

def get_dressed(tweets_df):
    #BEST DRESSEED
    best = ["(B|b)est dressed (?P<name>[A-Z][a-z]* [A-Z][a-z-]*)"]
            #"(?P<name>[A-Z][a-z]* [A-Z][a-z-]*) (best|BEST|Best) dressed"]
    bAW_func = [re.compile(b) for b  in best]
    names = tweets_df["text"].map(partial(dressed_helper, func=bAW_func, cat="best"))
    best_dressed = format_output(names)

    #WORST DRESSED
    worst = ["(W|w)orst dressed (?P<name>[A-Z][a-z]* [A-Z][a-z-]*)",
                  "(?P<name>[A-Z][a-z]* [A-Z][a-z-]*) (worst|WORST|Worst) dressed"]
    bAW_func = [re.compile(w) for w in worst]
    names = tweets_df["text"].map(partial(dressed_helper, func=bAW_func, cat="worst"))
    worst_dressed = format_output(names)

    f = ""
    if len(best_dressed) > 2:
        f+=f"Best Dressed: {best_dressed[0]}\nSecond Best Dressed: {best_dressed[1]}\n"
    elif len(best_dressed) == 1:
        f+=f"Best Dressed: {best_dressed[0]}\n"
    if len(worst_dressed) > 2:
        f += f"Worst Dressed: {worst_dressed[0]}\nSecond Worst Dressed: {worst_dressed[1]}\n"
    elif len(worst_dressed) == 1:
        f+=f"Worst Dressed: {worst_dressed[0]}\n"

    return f