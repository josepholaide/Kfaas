
import re, itertools, pickle
from datetime import datetime, timedelta
import pandas as pd

import snscrape.modules.twitter as sntwitter

import pymongo
from pymongo import MongoClient

def tweets_scape():
    # our search term, using syntax for Twitter's Advanced Search
    today = datetime.now().date()
    past = timedelta(36)

    tickers = ['AMZN', 'TSLA', 'MSFT', 'AAPL', 'Stocks', 'Crypto', 'Stock Market', 'Stock Trading']
    all_data = []

    for i in tickers:
      search = f'{i} lang:en since:{today-past} until:{today} -filter:links -filter:replies'

      # the scraped tweets, this is a generator
      scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()

      # slicing the generator to keep only the first 3000 tweets
      sliced_scraped_tweets = itertools.islice(scraped_tweets, 3000)

      # convert to a DataFrame and keep only relevant columns
      df = pd.DataFrame(sliced_scraped_tweets)[['date',	'content']]
      df['Tick'] = i
      print(i)
      all_data.append(df)

    all_data = pd.concat(all_data, ignore_index=True)
    data = all_data.to_dict(orient="records")

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
        collection = db.news.tweets
        collection.insert_many(data)
    except:
        print('Mongodb not connected')

if __name__ == '__main__':
  tweets_scape()
