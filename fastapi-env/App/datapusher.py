from typing import Optional
import requests
from endpoints import bearer,headers,URLS
from fastapi import FastAPI,Depends
from database import engine,SessionLocal
from model import Base,tweet
from sqlalchemy.orm import Session
import sqlite3

def dataPusher(data,id):
    conn = sqlite3.connect("tweet.db")
    cursor=conn.cursor()
    for objs in data:
        try:
            cursor.execute("insert into tweets values ( ?, ?, ?)", (objs['id'],id,str(objs['text']) ))
        except:
            print("" ,end='')
    print("Data Inserted in the table: ")
    
    conn.commit()
    conn.close()
    return "Success"
