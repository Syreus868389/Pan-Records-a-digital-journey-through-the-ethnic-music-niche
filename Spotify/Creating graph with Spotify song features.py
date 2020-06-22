# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 22:24:38 2020

@author: Théo
"""
#This script is heavily inspired by those made available by GitHub user lucadp19 at 
#https://github.com/lucadp19/SpotifyPlaylistUnion and by GitHub user aryajpandey at 
#https://github.com/aryajpandey/Spotipy_album_analysis/blob/master/analysis.ipynb

import spotipy 
import numpy as np
import json
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt

# spotify authentication and initialization of client object
client_id = '#################'
client_secret = '##################'
redirect_uri = '##########'
username = '##############'
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

#refresh function
def refresh():
    global token_info, sp

    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        token = token_info['access_token']
        sp = spotipy.Spotify(auth=token)

#function to get the uris of every track in a playlist
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
        refresh()
        return tracks
    except:
          pass
    
#function to get every track for the playlists returned by a query
def get_tracks (query, username):
    results=sp.search(query,limit=50,type='playlist') 
    refresh()
    items=results['playlists']['items']
    uris=[]
    for item in items:
        uri=item['uri']
        uris.append(uri)
    track_list=[]
    every_track=[]
    for uri in uris:
        tracks=get_playlist_tracks(username, uri)
        refresh()
        try:
            for track in tracks:
                track_list.append(track)
        except:
            pass
    for track in track_list:
        try:
            tracks=sp.track(track)
            every_track.append(tracks)            
        except:
            pass
    return every_track

# function for getting song features from playlist tracks
def get_features_for_query(name,tracks):
    refresh()
    print('getting features:%s'%name)
        # initialize the dictionary
    playlist_name = name
    plists[playlist_name] = {}
    plists[playlist_name]['name'] = []
    plists[playlist_name]['track uri'] = []
    plists[playlist_name]['acousticness'] = []
    plists[playlist_name]['danceability'] = []
    plists[playlist_name]['energy'] = []
    plists[playlist_name]['instrumentalness'] = []
    plists[playlist_name]['liveness'] = []
    plists[playlist_name]['loudness'] = []
    plists[playlist_name]['speechiness'] = []
    plists[playlist_name]['tempo'] = []
    plists[playlist_name]['valence'] = []
    plists[playlist_name]['popularity'] = []
    for track in tracks:
        name = track['name']
        track_uri = track['uri']          
        try:
            features = sp.audio_features(track_uri)
            # extract features
            refresh()
            plists[playlist_name]['acousticness'].append(features[0]['acousticness'])
            plists[playlist_name]['danceability'].append(features[0]['danceability'])
            plists[playlist_name]['energy'].append(features[0]['energy'])
            plists[playlist_name]['instrumentalness'].append(features[0]['instrumentalness'])
            plists[playlist_name]['liveness'].append(features[0]['liveness'])
            plists[playlist_name]['loudness'].append(features[0]['loudness'])
            plists[playlist_name]['speechiness'].append(features[0]['speechiness'])
            plists[playlist_name]['tempo'].append(features[0]['tempo'])
            plists[playlist_name]['valence'].append(features[0]['valence'])
            plists[playlist_name]['name'].append(name)
            plists[playlist_name]['track uri'].append(track_uri)
        except:
            continue
    
#getting tracks for the queries
world_music_tracks=[]
queries_world=['world music','wereld muziek','musique du monde']
for query in queries_world:
    results=get_tracks(query, username)
    for track in results:
        world_music_tracks.append(track)
    refresh()
    
print('world done')
    
folk_music_tracks=[]
queries_folk=['folk music','volksmuziek','musique folklorique']
for query in queries_folk:
    results=get_tracks(query, username)
    for track in results:    
        folk_music_tracks.append(track)
    refresh()
    
print('folk done')
    
ethnic_music_tracks=[]
queries_ethnic=['ethnic music','etnische muziek','musique ethnique']
for query in queries_ethnic:
    results=get_tracks(query, username)
    for track in results:     
        ethnic_music_tracks.append(track)
    refresh()
    
print('ethnic done')
    
trad_music_tracks=[]
queries_trad=['traditional music','traditionele muziek','musique traditionnelle']
for query in queries_trad:
    results=get_tracks(query, username)
    for track in results:
        trad_music_tracks.append(track)  
    refresh()

print('trad done')

pan_tracks=[]
pan_playlist=get_playlist_tracks(username,'spotify:playlist:1U0coxWGW7h3wIec2Y1mQi')
for track in pan_playlist:
    try:
        tracks=sp.track(track)
        pan_tracks.append(tracks)    
    except:
        pass


print('querying part 1 done')
    
plists = {}

#getting features for every cluster of tracks
queries_all=[world_music_tracks, folk_music_tracks, ethnic_music_tracks, trad_music_tracks, pan_tracks] 
name_list=['World','Folk','Ethnic','Traditional','Pan Records']
for i in range(0, len(queries_all)):
        name=name_list[i]
        print(name)
        tracks=queries_all[i]
        get_features_for_query(name,tracks)


#making a graph with the results
for playlist in plists:
    print("––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––")
    print(playlist)
    for feature in plists[playlist]:
        if feature != 'name' and feature != 'track uri':
            print(feature.upper(), "| median:", np.median(plists[playlist][feature]), "| mean:", np.mean(plists[playlist][feature]))


labels = ['acousticness', 'danceability', 'energy', 'valence', 'instrumentalness', 'tempo', 'speechiness']
num_vars = len(labels)

# Split the circle into even parts and save the angles so we know where to put each axis.
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angles += angles[:1]

# ax = plt.subplot(polar=True)
fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

# Helper function to plot each playlist on the radar chart.
def add_to_radar(playlist, color):
    values = [np.median(plists[playlist]['acousticness']), np.median(plists[playlist]['danceability']), np.median(plists[playlist]['energy']), 
              np.median(plists[playlist]['valence']), np.mean(plists[playlist]['instrumentalness']), np.median(plists[playlist]['tempo']), 
              np.median(plists[playlist]['speechiness'])]
    # tempo values typically range from 50-220, so I divided by 220 to get a number between 0 and 1
    values[-2] = values[-2]/220
    # speechiness values values are highly concentrated between 0 and 0.25-ish, so I multiplied by 4. Adjust this if needed
    values[-1] = values[-1]*4
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=1, label=playlist)
    ax.fill(angles, values, color=color, alpha=0.25)

# # Add each additional playlist to the chart.
add_to_radar('World', 'red')
add_to_radar('Folk', 'green')
add_to_radar('Ethnic','blue')
add_to_radar('Traditional','yellow')
add_to_radar('Pan Records', 'purple')

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Draw axis lines for each angle and label.
ax.set_thetagrids(np.degrees(angles), labels)

# Go through labels and adjust alignment based on where it is in the circle.
for label, angle in zip(ax.get_xticklabels(), angles):
  if angle in (0, np.pi):
    label.set_horizontalalignment('center')
  elif 0 < angle < np.pi:
    label.set_horizontalalignment('left')
  else:
    label.set_horizontalalignment('right')
    
# Set position of y-labels (0-100) to be in the middle of the first two axes.
ax.set_ylim(0, 1)
ax.set_rlabel_position(180 / num_vars)

ax.tick_params(colors='#222222')         # color of tick labels
ax.tick_params(axis='y', labelsize=8)    # y-axis labels
ax.grid(color='#AAAAAA')                 # color of circular gridlines
ax.spines['polar'].set_color('#222222')  # color of outermost gridline (spine)
ax.set_facecolor('#FAFAFA')              # background color inside the circle itself

#Lastly, give the chart a title and a legend
ax.set_title('Playlist Comparison', y=1.08)
ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))

plt.savefig('Graph_Cluster_comparison.png')
