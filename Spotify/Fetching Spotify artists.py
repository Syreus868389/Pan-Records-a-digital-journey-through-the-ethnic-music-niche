# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 18:08:09 2020

@author: Théo
"""
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import csv
import pandas as pd


# spotify authentication and initialization of client object
client_id = '#############'
client_secret = '###########'
redirect_uri = '#############'
username = '###############'
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

results_2=sp.search('musique folk',limit=50, type='playlist')
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
        return tracks
    except:
          pass
       
  
artist_names=[]  

# getting artist names from all playlists  
for playlist in source_playlists:
    while True:
        try:
            tracks=get_playlist_tracks(username,playlist)
            try:
                for track in tracks:
                        tracks=sp.track(track)
                        for artist in tracks['artists']:
                            artist_name=artist['name']
                            print(artist_name)
                            artist_names.append(artist_name)
            except: 
                pass
        except:
            refresh()
            continue
        break

list1=artist_names      
list2 = [] 
  
# making a list of names without duplicates
for i in list1:              
        if i not in list2: 
            list2.append(i)  
              
# counting the frequency of artist names and writing to csv file
for i in range(0, len(list2)):
    if i not in list2:
        with open('artist_names_folk.csv','a', encoding='utf-8') as csvfile:
            freqwriter = csv.writer(csvfile, delimiter=',')
            freqwriter.writerow([list2[i]]+[list1.count(list2[i])])
else:
    None

# converting csv file to excel file
Name_List=['Artist','Frequency']
df = pd.read_csv("artist_names_folk.csv", names=Name_List)

pd.DataFrame(df).to_excel('artist_names_folk.xlsx')