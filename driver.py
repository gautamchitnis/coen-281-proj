import json
import mysql.connector
from utils.TweetCleaner import TweetCleaner
from utils.SaveStream import SaveStream


if __name__ == '__main__':
    print("Start Data Generation")
    saveStream = SaveStream()

    data = saveStream.get_recent_stream(count=5)

    ch = 2

    if ch == 0:
        try:
            with open('data.json', 'w') as f:
                f.write(json.dumps(data, indent=4))
                print("Data Generation Complete")
        except BaseException as e:
            print("Error : %s" % str(e))
    elif ch == 1:
        dbConn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root1234",
            database="coen281"
        )

        dbCursor = dbConn.cursor()
        sql = "INSERT INTO tweets VALUES (%s, %s, %s)"

        for tweet_id in data:
            val = [int(tweet_id), int(data[tweet_id]["author_id"]), data[tweet_id]['text']]
            dbCursor.execute(sql, val)
            dbConn.commit()

    if ch == 2:
        my_result = TweetCleaner().read_db()
        # dbConn = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="root1234",
        #     database="coen281"
        # )
        # dbCursor = dbConn.cursor()
        # dbCursor.execute("SELECT * FROM tweets")

    # my_result = dbCursor.fetchall()
        token = TweetCleaner().cleaning(my_result)
        stop_words = TweetCleaner().tokenizer(token)
        add_db = TweetCleaner().stop_word(stop_words)
        TweetCleaner().add_clean_data(add_db, my_result)