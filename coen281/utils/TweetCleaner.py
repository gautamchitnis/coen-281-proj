import mysql
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import string
from nltk.stem import PorterStemmer


class TweetCleaner:
    def __init__(self):
        nltk.download('stopwords')

    def clean(self, tweet):
        cleaned_data = []
        data = tweet

        removed_rt = re.sub(r'^RT[\s]+', '', data)  # it will remove the old style retweet text "RT"
        remove_hyper = re.sub(r'https?:\/\/.*[\r\n]*', '', removed_rt)  # it will remove hyperlinks
        remove_hash = re.sub(r'#', '', remove_hyper)  # it will only remove hashtags.
        remove_no = re.sub(r'[0-9]', '', remove_hash)
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        cleaned_data.append(emoji_pattern.sub(r'', remove_no))  # removing emojis from tweets

        tokens = self.tokenizer(cleaned_data)

        clean_tweet = self.stop_word(tokens)

        return clean_tweet

    def tokenizer(self, cleaned_data):
        tweet_tokens = []
        for row in cleaned_data:
            # instantiate the tokenizer class
            # tokenize the tweets
            tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
            tweet_tokens.append(tokenizer.tokenize(row))
        return tweet_tokens

    def stop_word(self, tweet_tokens):
        stpwrd = stopwords.words('english')
        new_stopwords = [":)", ":/", "to", "on"]
        stpwrd.extend(new_stopwords)
        clean_tweet = []

        for word in tweet_tokens:  # Go through every word in your tokens list
            clean = []
            for x in word:
                if (x not in stpwrd and  # remove stopwords
                        x not in string.punctuation):  # remove punctuation
                    clean.append(x)
            clean_tweet.extend(clean)
        return clean_tweet
