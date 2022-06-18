import pickle

import argparse, time
from pathlib import Path

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import yfinance as yf

time.sleep(5)
def news_scape(args):
    yahoo_fin = 'https://finance.yahoo.com/quote/{ticker}/news?p={ticker}'

    # Gets and split dataset
    tickers = ['AMZN', 'TSLA', 'GOOG', 'FB', 'MSFT', 'AAPL']
    
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
        df = pd.DataFrame(df_data, columns=["ticker", "Date", "Time", "News"])
        return df
    
    newdf = []
    for i in tickers:
        df = scrape(f'/content/{i}.html', i)
        newdf.append(df)

    data = new_df.to_dict(orient="records")
        
    #Save the train_data and test_data as a pickle file to be used by the next component.
    with open(args.data, 'wb') as f:
        pickle.dump(data, f)

if __name__ == '__main__':
    
    # This component does not receive any input
    # it only outpus one artifact which is `data`.
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str)
    
    args = parser.parse_args()
    
    # Creating the directory where the output file will be created 
    # (the directory may or may not exist).
    Path(args.data).parent.mkdir(parents=True, exist_ok=True)

    news_scape(args)
    
