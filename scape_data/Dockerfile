FROM ubuntu:latest
WORKDIR /nlp
RUN apt-get -y update
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip -y
RUN pip install --upgrade pip
RUN apt install chromium-chromedriver -y
RUN pip install selenium yfinance
RUN apt-get -y update
COPY news_scape.py /nlp
