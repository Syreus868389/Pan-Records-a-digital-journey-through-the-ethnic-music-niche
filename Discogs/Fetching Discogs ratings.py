# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 00:11:45 2020

@author: Théo
"""

import csv
import pandas as pd
import time as t
import requests
from requests_oauthlib import OAuth1
import json 

import discogs_client

# client keys from API client
consumer_key = '#######'
consumer_secret = '#######'

# Defining API user_agent
user_agent = 'name_of_API_user_agent'

# instantiate Discogs_client object
discogsclient = discogs_client.Client(user_agent)

# prepare the client with API consumer data and getting authorize_url
discogsclient.set_consumer_key(consumer_key, consumer_secret)
token, secret, url = discogsclient.get_authorize_url()

# getting token and token_secret from requests package
print (' == Request Token == ')
oauth_token='{0}'.format(token)
print ('    * oauth_token        = ', oauth_token)
oauth_token_secret='{0}'.format(secret)
print ('    * oauth_token_secret = ', oauth_token_secret)
print

# defining authentication object for calling API through requests package
auth = OAuth1(consumer_key, consumer_secret, oauth_token, oauth_token_secret)

# getting a list of the label releases through Discogs client
label = discogsclient.label(######)
releases = label.releases

# initiating lists
ratings=[]
counts=[]
years=[]

# getting ratings from API through requests package, with a sleep time to avoid rate limiting
for release in releases:
    number=release.id
    url='https://api.discogs.com/releases/{0}/rating'.format(number)
    resp=requests.get(url,auth=auth)
    results=resp.text
    resultso=json.loads(results)
    rating=resultso['rating']['average']
    ratings.append(rating)
    count=resultso['rating']['count']
    counts.append(count)
    url_2='https://api.discogs.com/releases/{0}'.format(number)
    resp_2=requests.get(url_2,auth=auth)
    results_2=resp_2.text
    resultso_2=json.loads(results_2)
    year=resultso_2['year']
    years.append(year)
    t.sleep(5)


list1=ratings
list2=counts
list3=years
   
# writing lists to csv
with open('discogs_ratings.csv','a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in range(len(list1)):
            writer.writerow([list1[i]]+[list2[i]]+[list3[i]])
        
# converting csv to excel
Name_List=['Rating','Count','Year']
df = pd.read_csv("discogs_ratings.csv", names=Name_List)

pd.DataFrame(df).to_excel('discogs_ratings.xlsx')
                    
