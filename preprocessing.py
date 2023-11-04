import pandas as pd


def preproccessing(json_file="gg2013.json"):
    data_frame = pd.read_json(json_file)

    # seperate into columns
    data_frame = data_frame[["text", "timestamp_ms"]]

    # seperating time from ms to date format
    data_frame["timestamp"] = pd.to_datetime(data_frame["timestamp_ms"], unit='ms')

    # cleaning up the text for any not standard language characters
    data_frame["text"] = (
        data_frame["text"].str.replace("[^a-zA-Z-\\s]", "", regex=True).str.strip()
        )
    

    # keep only tweets in english
    with open("100CommonWords.txt", 'r') as file:
        common_english_words = set(file.read().splitlines())
        # list from https://gist.github.com/deekayen/4148741
        # had to use a list since I couldn't get any language detector to install/work properly
    def is_english(text):
        # is english if any words in tweet match any of the most common 100, if word length >= 2
        words = text.split()
        return any(word in common_english_words for word in words if len(word) >= 2)
        
    # delete any rows that are not in english
    data_frame["is_english"] = data_frame["text"].apply(is_english)
    data_frame = data_frame[data_frame['is_english']]

    # removing empty tweets and duplicates
    data_frame.drop_duplicates(subset=['text'], inplace=True)
    data_frame.dropna(subset=['text'], inplace=True)

    # save data frame to json so we don't have to preprocess over and over
    new_file = json_file.split(".")[0] + "_preprocessed.json"
    data_frame.to_json(new_file, orient='records', lines=True)
    return data_frame

#preproccessing()