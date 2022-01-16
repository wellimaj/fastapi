from database import Base
from pydantic import BaseModel
from sqlalchemy import Column,Integer,String


class tweet(Base):
    __tablename__='tweets'
    twitid=Column(String,primary_key=True,index=True)
    id=Column(String)
    title =Column(String)
class tweetSchema(BaseModel):
   
    twitid:str
    id:str
    title :str