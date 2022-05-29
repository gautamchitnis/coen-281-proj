import json
import mysql.connector

from coen281.utils import SaveStream


if __name__ == '__main__':
    print("Start Data Generation")
    saveStream = SaveStream()

    data = saveStream.get_recent_stream(count=5)

    ch = 1

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
