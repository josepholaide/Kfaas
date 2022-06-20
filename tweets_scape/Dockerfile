FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /
RUN pip install pandas snscrape dnspython pymongo==3.7.2
COPY tweets_scape.py /
