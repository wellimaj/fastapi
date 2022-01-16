import sqlite3
import json
def dataFetcher(keyword,user):
    conn = sqlite3.connect("tweet.db",check_same_thread=False)
    cursor=conn.cursor()
    data=cursor.execute(f'''SELECT * FROM tweets 
WHERE (title LIKE '%{keyword}%') and id='{user}' ''')
    print(type(data))
    list=[]
    for x in data:
        list.append(x)
    conn.commit()
    conn.close()
    return list
    