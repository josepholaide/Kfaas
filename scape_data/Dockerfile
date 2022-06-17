FROM python:3.9-slim-buster
WORKDIR /nlp
RUN apt-get -y update
RUN apt install chromium-chromedriver -y
RUN pip install selenium yfinance dnspython pymongo==3.7.2 -y
COPY news_scape.py /nlp
