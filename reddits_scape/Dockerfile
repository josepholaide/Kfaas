FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /
RUN pip install pandas praw dnspython pymongo==3.7.2
COPY reddits_scape.py /
ENTRYPOINT ["python", "/reddits_scape.py"]
