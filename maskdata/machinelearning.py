import json
import praw
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
from sklearn import metrics
import nltk
import sys

sys.setrecursionlimit(3000)
# imports for text processing
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re

import os
from incognito.settings import BASE_DIR



class MachineLearning:
    file_path = os.path.join(BASE_DIR, 'maskdata/incognito.model')
    print("This is the filepath ***********"+file_path)
    with open(file_path, 'rb') as f:
        incognito = pickle.load(f)
    file_path = os.path.join(BASE_DIR, 'maskdata/vectorizer')
    with open(file_path, 'rb') as f:
        vectorizer = pickle.load(f)

    def __init__(self):
        file_path = os.path.join(BASE_DIR, 'maskdata/incognito.model')
        print("This is the filepath ***********" + file_path)
        with open(file_path, 'rb') as f:
            incognito = pickle.load(f)
        file_path = os.path.join(BASE_DIR, 'maskdata/vectorizer')
        with open(file_path, 'rb') as f:
            vectorizer = pickle.load(f)

    def getdata(subreddit):


        reddit = praw.Reddit(client_id='RftLG9CCeSuWXA',
                             client_secret='QekfUYq0g_C0RCJFdn6QOCdxhKg',
                             redirect_uri='http://localhost:8080',
                             user_agent='Incognito')

        df = pd.DataFrame(columns=['id','subreddit', 'Author', 'Title', 'Content', 'url', 'Comments', 'NumberOfComment',
                                   'Upvote_Count', 'CreatedAt'])
        # get 10 hot posts from the MachineLearning subreddit
        hot_posts = reddit.subreddit(subreddit).controversial(limit=10)

        for post in hot_posts:
            submission = reddit.submission(id=post.id)

            comments = []
            submission.comments.replace_more(limit=0)
            for comment in submission.comments:
                comments.append([str(comment.body), str(comment.author)])

            df = df.append(
                {'id':submission.id,'subreddit': str(submission.subreddit), 'Author': str(submission.author), 'Title': submission.title
                    , 'Content': submission.selftext, 'url': submission.url, 'Comments': comments,
                 'NumberOfComment': len(comments)
                    , 'Upvote_Count': submission.score, 'CreatedAt': datetime.fromtimestamp(submission.created_utc)}
                , ignore_index=True)

        return df

    def predict(text):
        vectorized_text = MachineLearning.vectorizer.transform([text])
        result = MachineLearning.incognito.predict(vectorized_text)

        if result[0] == 1:
            return 'bullying content found, text deleted!'

        return text

    def dothething(subredditname='pubg'):

        df = MachineLearning.getdata(subredditname)
        df=df.set_index('id')
        df['Title'] = df['Title'].apply(MachineLearning.predict)
        df['Content'] = df['Content'].apply(MachineLearning.predict)
        for i in range(0, len(df['Comments'])):
            for j in range(0, len(df['Comments'][i])):
                df['Comments'][i][j][0] = MachineLearning.predict(df['Comments'][i][j][0])

        #df.to_json('Third.json')
        #with open('Third.json', 'r') as f:
        #    datastore = json.load(f)
        #print(df.Content)
        return df.to_dict(orient='index')



