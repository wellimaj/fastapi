import sqlite3

def dataPusher(data,id):
    conn = sqlite3.connect("tweet.db")
    cursor=conn.cursor()
    for objs in data:
        print(objs)
        try:
            cursor.execute("insert into tweets values ( ?, ?, ?)", (objs['id'],id,str(objs['text']) ))
            print("Data Inserted in the table: ")
        except Exception as e:
            print(e)
       
    
    
    conn.commit()
    conn.close()
    return "Success"
