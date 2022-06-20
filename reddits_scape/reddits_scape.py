
from datetime import datetime
import pandas as pd

import praw
from praw.models import MoreComments

import pymongo
from pymongo import MongoClient

def reddit_scape():
    # initialize Reddit scraping API
    reddit = praw.Reddit(client_id='y_Npzkw006QBHn5PdyOOxw', client_secret='YvlY1LRvjm7G3MXz1QQ4k4aMvr3q3w', user_agent='scraper')

    # subreddits to scrape
    subreddits = ['TSLA', 'Coinbase', 'Cryptocurrency', 'Crypto', 'Trading', 'robinhood', 'Finance', 'Bloomberg', 'Stocks', 'Investing']
    
    posts = []
    
    # loop through subreddits
    for i in subreddits:
      ml_subreddit = reddit.subreddit(i)
      # extract subreddit content
      for post in ml_subreddit.hot(limit=1200):
          posts.append([post.title, post.score, post.id, post.subreddit, post.num_comments, post.selftext, post.created_utc])
    
    # create a dataframe of all contents
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'num_comments', 'body', 'created'])

    # extract datetime column
    posts['created'] = posts['created'].apply(datetime.utcfromtimestamp).dt.date
    posts['created'] = pd.to_datetime(posts['created'])

    # sort by date create
    posts = posts.sort_values(by='created', ascending=False)

    # filter by date
    posts = posts[posts['created'] >= "2022-05-01"]
    
    # get comments on each subreddit topic
    data = []
    j = 0
    for i in posts['id'].values:
      submission = reddit.submission(id=str(i))
      for top_level_comment in submission.comments:
          if isinstance(top_level_comment, MoreComments):
              continue
          data.append(top_level_comment.body)
    j+=1
    print(j)

    # add title to all comments
    data = list(posts['title'].values) + data

    # convert to dictionary
    all_data = {}
    all_data['content'] = data
    data_ = all_data.to_dict(orient="records")

    # uri (uniform resource identifier) defines the connection parameters 
    uri = 'mongodb+srv://josepholaide:1234@cluster0.bqed12j.mongodb.net/?retryWrites=true&w=majority'
    # start client to connect to MongoDB server 
    client = MongoClient(uri)

    try:
        # Show existing database names
        client.list_database_names()
        # Set database name to work with. If it doesn't exist, it will be created as soon as one document is added.
        db = client.finance
        # Set the collection to work with
        collection = db.news.reddit
        collection.insert_many(data_)
    except:
        print('Mongodb not connected')

if __name__ == '__main__':
  reddit_scape()