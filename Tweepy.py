#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tweepy
import pandas as pd
import json


# In[3]:


consumer_key="Add_Your_Consumer_Key"
consumer_secret="Add_Your_Consumer_Secret"
access_token="Add_Your_Access_Token"
access_token_secret="Add_Your_Token_Secret"


# In[4]:


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)



# In[14]:


number_of_tweets=3500
tweets=[]
likes=[]
time=[]

for i in tweepy.Cursor(api.user_timeline, id="OgeroTelecom",tweet_mode="extended").items(number_of_tweets):
    tweets.append(i.full_text)
    likes.append(i.favorite_count)
    time.append(i.created_at)


# In[15]:


df = pd.DataFrame({'tweets':tweets,'likes':likes,'time':time})


# In[17]:


df = df[~df.tweets.str.contains("@")]


# In[22]:


df = df[~df.tweets.str.contains("تمّ اصلاح العطل")]


# In[18]:


df = df[df.tweets.str.contains("عطل")]




# In[23]:


df = df[~df.tweets.str.contains("تم معالجة العطل")]
df


# In[27]:


df = df[~df.tweets.str.contains("تم اصلاح العطل")]


# In[25]:


df = df.reset_index(drop=True)











