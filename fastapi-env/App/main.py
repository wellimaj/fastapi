from typing import Optional
import requests
from endpoints import headers,URLS
from fastapi import FastAPI,Depends
from database import engine,SessionLocal
from model import Base,tweet,tweetSchema
from sqlalchemy.orm import Session
import time
from datafetcher import dataFetcher
app=FastAPI()
Base.metadata.create_all(engine)
from datapusher import dataPusher
@app.get('/v1/search/{user}')
def index(user):
    
    if user.isdigit():
        Userdata=requests.get(URLS.byId+user,headers=headers).json()
        print(True)
        return Userdata
    Userdata=requests.get(URLS.byUsername+user,headers=headers).json()
    
    return Userdata
@app.get('/v1/searchtweets/{user}')
def tweets(user):
    Userdata=requests.get("https://api.twitter.com/1.1/search/tweets.json?q="+user, 
headers=headers).json()
    print(type(Userdata["statuses"]))
    return Userdata
@app.get('/v1/{user}/{keyword}')
def tweethandler(user,keyword):
    
    if not user.isnumeric():
        user=requests.get(URLS.byUsername+user,headers=headers).json()["data"]["id"]
    token='&pagination_token='
    temp=""
    for x in range(5):
        
        if x==0:
            data=requests.get(URLS.byIDandUser+user+URLS.byIDandUserafter,headers=headers).json()
            
            if "next_token" in data["meta"]:
                temp=token+data['meta']["next_token"]
            dataPusher(data['data'],user)
        else:
            data=requests.get(URLS.byIDandUser+user+URLS.byIDandUserafter+temp,headers=headers).json()
            print("hi")
            if "next_token" in data["meta"]:
                temp=token+data['meta']["next_token"]
            
            data=data['data']
            dataPusher(data,user)
            time.sleep(0.1)
    result =dataFetcher(keyword,user) 
        
    return result if result else f"looks like user with ID:{user} doesnt really tweet regarding {keyword}"

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post('/tweet')
def create(request:tweetSchema,db : Session = Depends(get_db)):
    print(request)
    newtweet=tweet(id=request.id,twitid=request.twitid,title=request.title)
    db.add(newtweet)
    db.commit()
    db.refresh(newtweet)
    return newtweet

