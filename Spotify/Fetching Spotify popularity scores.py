# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 23:29:38 2020

@author: Théo
"""

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import csv
import pandas as pd
import statistics


# spotify authentication and initialization of client object
client_id = '############'
client_secret = '###########'
redirect_uri = '###############"'
username = '###########'
scopes = 'playlist-modify-private'

sp_oauth = SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scopes)
token_info = sp_oauth.get_cached_token() 
if not token_info:
    auth_url = sp_oauth.get_authorize_url(show_dialog=True)
    print(auth_url)
    response = input('Paste the above link into your browser, then paste the redirect url here: ')

    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

    token = token_info['access_token']

sp = spotipy.Spotify(auth=token)

# refresh function
def refresh():
    global token_info, sp

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        token = token_info['access_token']
        sp = spotipy.Spotify(auth=token)

uris=[]

# getting playlists for query
results=sp.search('folk music',limit=50,type='playlist') 
items=results['playlists']['items']
for item in items:
    uri=item['uri']
    uris.append(uri)

results_1=sp.search('volksmuziek',limit=50, type='playlist')
items_1=results_1['playlists']['items']
for item in items_1:
    uri=item['uri']
    uris.append(uri)

results_2=sp.search('musique folklorique',limit=50, type='playlist')
items_2=results_2['playlists']['items']
for item in items_2:
    uri=item['uri']
    uris.append(uri)

count=len(uris)
print(count)

source_playlists=uris

# fetching the tracks from the playlist
def get_playlist_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    try:
        tracks = [t['track']['id'] for t in results['items']]
        while results['next']:
              results = sp.next(results)
              try:
                 tracks.extend([t['track']['id'] for t in results['items']])
              except:
                   pass
    except:
          pass
    return tracks
       
  
popularities=[]  

# getting popularity for every track
for playlist in source_playlists:
    while True:
        try:
            tracks=get_playlist_tracks(username,playlist)
            try:
                for track in tracks:
                    tracks=sp.track(track)
                    popularity=tracks['popularity']
                    print(popularity)
                    popularities.append(popularity)
            except: 
                pass
        except:
            refresh()
            continue
        break


#calculating the mean of the popularity scores
mean=statistics.mean(popularities)
print('mean:',mean)
    