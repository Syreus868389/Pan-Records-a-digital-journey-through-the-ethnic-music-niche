# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 18:19:30 2020

@author: Théo
"""
import json
from requests_oauthlib import OAuth1Session
from flask import Flask, request, redirect, session, url_for
import discogs_client
import time as t
import csv
import pandas as pd

# defining credentials
user_agent = '########'
client_key='######'
client_secret='#######'

# instantiate discogs_client object
discogsclient = discogs_client.Client(user_agent)
discogsclient.set_consumer_key(client_key, client_secret)
token, secret, url = discogsclient.get_authorize_url()


request_token_url ='https://api.discogs.com/oauth/request_token'
base_authorization_url = 'https://www.discogs.com/oauth/authorize'
access_token_url='https://api.discogs.com/oauth/access_token'

#instantiate OAuth object
oauth = OAuth1Session(client_key, client_secret=client_secret)
fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

authorization_url = oauth.authorization_url(base_authorization_url)
print ('Please go here and authorize,', authorization_url)
verifier = input('Paste the verifier here: ')


oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=verifier)
oauth_tokens = oauth.fetch_access_token(access_token_url)
resource_owner_key = oauth_tokens.get('oauth_token')
resource_owner_secret = oauth_tokens.get('oauth_token_secret')

# get releases of the label (Pan Records in this case)
label = discogsclient.label(111486)
releases = label.releases
print(releases)

# fetch price sugestion values, with a sleep time to avoid rate limiting
titles=[]
values=[]
for release in releases:
    id=release.id
    resp=oauth.get('https://api.discogs.com/marketplace/price_suggestions/{0}'.format(id))
    results=resp.text
    resultso=json.loads(results)
    try:
        if resultso['Mint (M)']:
            value=resultso['Mint (M)']['value']
            print(value)
            values.append(value)
            title=release.title
            print(title)
            titles.append(title)
        if not resultso['Mint (M)']:
            pass
    except:
        pass
    t.sleep(5)

# write the titles of the songs with their suggested value in csv and then xlsx files
with open('price_suggestions.csv','a', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for i in range(0,len(titles)):
            writer.writerow([titles[i]]+[values[i]])

Name_List=['Release','Value suggestion']
df = pd.read_csv("price_suggestions.csv", names=Name_List)

pd.DataFrame(df).to_excel('price_suggestions.xlsx')
    


