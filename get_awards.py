def get_all_awards(tweets):
    preprocessed_tweets = "gg2013_preprocessed.json"
    tweets = pd.read_json(preprocessed_tweets, orient='records', lines=True)[["text","is_english"]]
    tweets = tweets[tweets["is_english"]] #only keep english tweets
    del tweets["is_english"] #get rid of this row
    tweets = tweets.dropna(subset=["text"])
    def extract_person_entities(texts):
        nlp = spacy.load("en_core_web_lg", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])
        removed_entities = []
        # remove any string that isn't the correct part of speech 
        missing_pos = {'AUX', 'CONJ', 'INTJ', 'NUM', 'PART', 'PRON', 'SCONJ', 'SYM', 'X'}
        for text in texts:
            doc = nlp(text.replace(" -", "").strip())
            has_missing_pos = False  # flag to check if a text contains a missing part of speech
            
            # check if the text contains any of the missing parts of speech
            for token in doc:
                if token.pos_ in missing_pos:
                    has_missing_pos = True
                    break
            
            # if the text contains a missing part of speech, skip it
            if has_missing_pos:
                # print("Skipped due to missing POS |", text)
                continue
            
            if len(doc.ents) > 0:
                for ent in doc.ents:
                    if ent.label_ == 'PERSON':
                        if " - " + ent.text in text:
                            new_text = text.split(" - " + ent.text, 1)[0]
                        else:
                            new_text = text.split(ent.text, 1)[0]
                        # print(ent.text, "|", text, "|", new_text)
                        removed_entities.append(new_text.strip())
                        break
                    # else:
                        # print("no people |", ent.text, "|", text)
                        # removed_entities.append(text)
            else:
                # print("no ents |", text.replace("-", "").strip())
                removed_entities.append(text)

        # print(len(removed_entities))
        return removed_entities

    def clean_and_sort_text(text):
        # function to group award names, even if they are missing a key word or a "-"
        words = re.sub(r"(motion|original|-)", "", text).split()
        # sort words and join back into a string
        return ' '.join(sorted(words))

    extracted_award_names = []
    # indentify which tweets might contain an award name
    keywords = ['best']
    pattern = '|'.join(keywords)
    candidate_tweets = df[df[text_column].str.contains(pattern, regex=True)]

    # matching regex to all the tweets
    regex_pattern = r"\b(wins|awarded|goes to) (.*?)(award)?($|[,.!?:;])"
    for tweet in candidate_tweets[text_column]:
        matches = re.findall(regex_pattern, tweet)
        if len(matches) > 0:
            for match in matches:
                award_name = match[1].strip()
                extracted_award_names.append(award_name)
        else:
            extracted_award_names.append(tweet)
    # clean up the results so we can rank them
    delimiters = r"(\shttp|\sat\s|\sodds-on|\sgolden.*|\sglobe.*|\stony.*|\semm.*|\sand|\sgoes|\sof\s|\sfor\s(?!t)|\sdid)"
    cleaned_award_names = [re.split(delimiters, name)[0] for name in extracted_award_names]
    cleaned_award_names = ["-".join(name.split("-", 2)[:2]).strip() for name in cleaned_award_names if name.lower().startswith('best ')]
    # print(len(cleaned_award_names))
    cleaned_award_names = extract_person_entities(cleaned_award_names)
    cleaned_award_names = [re.sub("  ", "", name) for name in cleaned_award_names if len(name.split()) > 3]
    cleaned_award_names = [re.split(delimiters, name)[0] for name in cleaned_award_names]
    cleaned_award_names = ["-".join(name.split("-", 2)[:2]).strip() for name in cleaned_award_names if name.lower().startswith('best ')]
    cleaned_award_df = pd.DataFrame(cleaned_award_names, columns=['Cleaned_Award_Name'])
    cleaned_award_counts = cleaned_award_df['Cleaned_Award_Name'].value_counts().reset_index()
    cleaned_award_counts.columns = ['Cleaned_Award_Name', 'Frequency']

    cleaned_award_counts['Sorted_Award_Name'] = cleaned_award_counts['Cleaned_Award_Name'].apply(clean_and_sort_text)
    
    # chooses the longest award name of the grouping
    def prefer_longer(series):
        # print(series)
        return max(series, key=len)

    # group by the cleaned and sorted award names and add the frequencies together
    grouped_award_counts = cleaned_award_counts.groupby('Sorted_Award_Name').agg({
        'Cleaned_Award_Name': prefer_longer,  # keep the longest version
        'Frequency': 'sum'  # add up their frequencies
    }).reset_index(drop=True)

    grouped_award_counts = grouped_award_counts.sort_values(by='Frequency', ascending=False).reset_index(drop=True)

    return list(grouped_award_counts['Cleaned_Award_Name'])[:27]