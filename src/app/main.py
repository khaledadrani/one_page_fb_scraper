from fastapi import FastAPI, Request
from facebook_scraper import get_posts
from pydantic import BaseModel,ValidationError, validator
from typing import Optional
import json

app = FastAPI()

from pymongo import MongoClient
from dotenv import load_dotenv
import os 

def connect_db(connection_string,verbose=False):
    ''' Utility to connect to Mongodb. 
    Make sure to put an environment variable containing the connection string.

    Args: 
        connection_string: str
    Return:
        db: Pymongo session to the db
    
    '''
    try:
        
        client = MongoClient()
        client = MongoClient(connection_string)
        db = client["fb_scraper"]
        if verbose:
            print("DB loaded with success, list of collections:\n",db.list_collection_names())
        return db
    except Exception as err:
        print(err)

load_dotenv(".env")
connection_string = os.environ.get("DB_CONNECTION")

db = connect_db(connection_string=connection_string ,verbose=False)


class ExtractPost(BaseModel):
    '''
    Request Model for scraping posts from nintendo facebook page.
    Refer to facebook_scraper repository for further details.

    fields:
        pages: how many pages to be scraped, recommended to be more than 2.
        extra_info: bool, get the post reactions if true
        options: a dict of options. Exemple: Set options={"comments": True} to extract comments
    '''
    pages: int = 3
    extra_info: Optional[bool] = False
    options: Optional[dict]

class FindPost(BaseModel):
    '''
    Request Model for scraping.
    Refer to pymongo and mongodb documentation for further details.

    Fileds:
        fields: fieldnames to be retrieved for each document
        query: find by a certain value of a field like post_id
        sort: bool, if true, sort documents according to sort_filed and sort_order
        limit: int, how many documents to be retrieved, if 0, there is no limit.
    '''
    fields: dict = { "post_id": 1, "text": 1 ,"timestamp":1, "time":1}
    query: dict = {"post_id":"4600162900068127"}

    
    sort: bool = False
    sort_field: str = "timestamp"
    sort_order: int = -1
    limit: int = 0

    # def validate_post(self):
    #     if time_sort == 0:
    #         if timestamp not in self['fields']:
    #             raise Exception("timestamp not in fields for time sort")

    #     return True

class DeletePost(BaseModel):
    delete_one: bool = False
    query: dict = {}


@app.get("/")
async def root():
    ''' A route for a simple test'''
    return {"message": "Hello World"}

@app.get("/stats/count_posts")
async def stats_count_posts():
    ''' Get the posts count in db'''
    return {"count_posts":db.posts.count_documents({})}


@app.post("/extract_posts")
async def extract_posts(request: ExtractPost):
    ''' Wrapper over facebook scraper open source library. 
    Scrape posts according to the ExtractPost request and add them to database if they do not exist already.
    '''
    
    request = json.loads(request.json())
    #print(request)

    init_nb = int(db.posts.find({}).count())
    messages = []

    #ls_posts = list(get_posts('nintendo',**request))
    #db.posts.insert_many(ls_posts,ordered=False)
    for post in get_posts('nintendo',**request):
        try: #insert_many ordered=False, causes a writingbulk error, need to investigate further
            db.posts.insert_one(post)
        except: 
            continue

    new_nb = int(db.posts.find({}).count())

    return {"new posts inserted":int(new_nb)-int(init_nb),"post count":int(new_nb)}
    
        
@app.post("/find_posts")
async def find_posts(request: FindPost):
    ''' wrapper over pymong. Retrieves posts data from database according to the FindPost request  '''
    try:
        
    
        request = json.loads(request.json())

        #print(request,type(request))

        query = request['query'] 
        fields = request['fields']
        fields['_id'] = fields.get('_id',0) #no need to get mongdb objectId

        sort = request['sort']
        sort_field = request['sort_field']
        sort_order = request['sort_order']
        limit = request['limit']
        
        if sort:
            ls_posts = db.posts.find(query,fields).sort(sort_field, sort_order).limit(limit)

        else:
            ls_posts = db.posts.find(query,fields).limit(limit)

        ls_posts= list(ls_posts)
        
        return {"posts":ls_posts}

    except Exception as e:
        return {"Exception":str(e)}


@app.post("/delete_posts")
async def delete_posts(request: DeletePost):
    ''' Delete one or many posts from database'''
    try:
        request = json.loads(request.json())

        query = request['query'] 

        delete_one = request['delete_one']

        if delete_one:

            res = db.posts.delete_one(query)

        else:

            res = db.posts.delete_many(query)
        
        return {"result":res.raw_result}

    except Exception as e:
        return {"Exception":str(e)}




