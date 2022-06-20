FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /
RUN pip install pandas selenium yfinance beautifulsoup4 dnspython pymongo==3.7.2
COPY news_scape.py /
