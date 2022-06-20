import pickle

import argparse, time
from pathlib import Path
import pandas as pd
from urllib.request import urlopen, Request

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from bs4 import BeautifulSoup
import yfinance as yf
import datetime                           
import pymongo
from pymongo import MongoClient

time.sleep(5)
def news_scape(args):
    yahoo_fin = 'https://finance.yahoo.com/quote/{ticker}/news?p={ticker}'

    # Gets and split dataset
    tickers = ['AMZN', 'TSLA', 'GOOG', 'MSFT', 'AAPL']
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # open it, go to a website, and get results
    driver = webdriver.Remote('http://selenium:4444/wd/hub',
                              desired_capabilities=options.to_capabilities())
    for i in tickers:
        driver.get(yahoo_fin.format(ticker=i))

        ScrollNumber = 50
        for j in range(1,ScrollNumber):
            driver.execute_script("window.scrollTo(1,50000)")
            time.sleep(5)
        print(i)
        file = open(f'{i}.html', 'w')
        file.write(driver.page_source)
        file.close()
        
    driver.close()
        
    def extract_information(link, ticker):
        try:
            if 'http' not in link:
                links = 'https://finance.yahoo.com/' + link
            else:
                links = link
            # open link    
            blogData = urlopen(Request(url=links, headers={'user-agent': 'chrome'})) 
            soup = BeautifulSoup(blogData, "html.parser", from_encoding="utf-8")
            # get headings
            heading = soup.find('h1').text
            # get body
            body = soup.find('div', attrs={'class': 'caas-body'}).find('p').text

            # join body and headings
            news = heading + '. ' + body 

            # get date ane time
            date = soup.find('time')['datetime'].split('T')[0]
            time = soup.find('time')['datetime'].split('T')[1].split('.')[0]
            return (ticker, date, time, news)
        except:
            pass
    def create_df(data):
        df = pd.DataFrame(data, columns=["ticker", "Date", "Time", "News"])
        return df

    def scrape(full_link, ticker):
        # open html file
        data = open(full_link, 'r')
        # pass html data to soup
        soup = BeautifulSoup(data, 'html.parser', from_encoding="iso-8859-1")
        # find unordered list
        ul_tag = soup.find('ul', attrs={'class': 'My(0) P(0) Wow(bw) Ov(h)'})

        df_data = []
        # find all links in lists
        for links in ul_tag.find_all('li'):
            link = links.find('a').get('href')
            df_data.append(extract_information(link, ticker))
        df = create_df(df_data)
        return df
    
    newdf = []
    for i in tickers:
        df = scrape(f'{i}.html', i)
        newdf.append(df)
        
    newdf_ = pd.concat(newdf, ignore_index=True)

    data = newdf_.to_dict(orient="records")
    
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
        collection = db.news
        collection.collection.insert_many(data)
    except:
        print('Mongodb not connected')
        
      
        
    #Save the train_data and test_data as a pickle file to be used by the next component.
    with open(args.data, 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    
    # This component does not receive any input
    # it only outpus one artifact which is `data`.
    parser = argparse.ArgumentParser()
    parser.add_argument("--data",
                      type=str,
                      default="data"
                      )
    
    args = parser.parse_args()
    
    # Creating the directory where the output file will be created 
    # (the directory may or may not exist).
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    news_scape(args)
    
