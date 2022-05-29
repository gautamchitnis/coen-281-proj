import mysql
import re
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
import string
from nltk.stem import PorterStemmer


class TweetCleaner():
    # def __init__(self, ch):
    #     self.ch = ch

    def read_db(self):
        dbConn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="coen281"
        )
        dbCursor = dbConn.cursor()
        dbCursor.execute("SELECT * FROM tweets")
        my_result = dbCursor.fetchall()
        return my_result

    def cleaning(self, my_result):
        cleaned_data = []
        for row in my_result:
            # print(" To be cleaned: ")
            data = row[2]
            # print(data)
            removed_rt = re.sub(r'^RT[\s]+', '', data)  # it will remove the old style retweet text "RT"
            # removed_rt = re.sub(r'^RT[\s]+', '', data[2])  # it will remove the old style retweet text "RT"
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
        return cleaned_data

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
        clean_tweets = []
        # tweets = []
        for word in tweet_tokens:  # Go through every word in your tokens list
            clean = []
            for x in word:
                # print(x)
                # print(type(x))
                if (x not in stpwrd and  # remove stopwords
                        x not in string.punctuation):  # remove punctuation
                    clean.append(x)
                # clean_tweets.append(tweets)
                # print(clean_tweets)
            clean_tweets.append(clean)
        return clean_tweets

    def add_clean_data(self, clean_tweets, my_result):
        dbConn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="coen281"
        )
        for idx, row in enumerate(my_result):
            dbCursor = dbConn.cursor()
            sql = "UPDATE tweets SET clean_tweet = %s WHERE tweet_id = %s"
            # sql = "UPDATE tweets SET clean_tweet = %s WHERE tweet_id = %s"
            a = ', '.join(clean_tweets[idx])
            val = a, row[0]
            dbCursor.execute(sql, val)
            dbConn.commit()
