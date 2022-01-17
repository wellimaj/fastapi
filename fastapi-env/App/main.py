import requests
from endpoints import headers,URLS
from fastapi import FastAPI
import time
from datafetcher import dataFetcher
app=FastAPI()

from datapusher import dataPusher

# main API takes user and keyword as path param
@app.get('/v1/custom/{user}/{keyword}')
def tweethandler(user,keyword):
    if keyword==f"{{keyword}}":
        return "no keyword entered"

    #tweets can be only searched by ID so converting username into ID here
    if not user.isnumeric():
        user=requests.get(URLS.byUsername+user,headers=headers).json()
        if "data" in user:
            user=user["data"]["id"]
        else:
            return "User suspended or does not exist"
    #logic to use pagination token for upto 5 pages with 10 volume, using low volume because only allowed 900 or something tweets per 15 minutes
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
           
            if "next_token" in data["meta"]:
                temp=token+data['meta']["next_token"]
            
            data=data['data']
            dataPusher(data,user)
            time.sleep(0.1)
    result =dataFetcher(keyword,user) 
        
    return result if result else f"looks like user with ID:{user} doesnt really tweet regarding {keyword}"

#< - additional stuff for testing purposes only - >
@app.get('/v1/search/{user}')
def index(user):
 
    
    if user.isdigit():
        Userdata=requests.get(URLS.byId+user,headers=headers).json()
     
        return Userdata
    Userdata=requests.get(URLS.byUsername+user,headers=headers).json()
    
    return Userdata
@app.get('/v1/searchtweets/{user}')
def tweets(user):
    Userdata=requests.get("https://api.twitter.com/1.1/search/tweets.json?q="+user, 
headers=headers).json()
   
    return Userdata


