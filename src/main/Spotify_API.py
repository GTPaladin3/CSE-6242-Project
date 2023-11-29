# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 18:32:58 2023

@author: spenc
"""

# pip install spotipy

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up your Spotify client credentials
client_id = '255ff85062be4aaaba1ec5fa597a8eea'
client_secret = '4b2241df02174c1eba41cc3293cd61f2'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Read your artist list from the CSV file
artists_df = pd.read_csv('C:/Users/spenc/Downloads/10000-MTV-Music-Artists.csv')

# Initialize lists to store track data and artists with errors
track_data_list = []
artists_with_errors = []

first_artist_name = artists_df.loc[0, 'name']
artist_list = [first_artist_name]


# Function to fetch the top tracks for an artist
def get_top_tracks(artist_id, country_code='US', total_limit=100):
    top_tracks = []
    unique_song_ids = set()
    offset = 0

    while offset < total_limit:
        try:
            limit = min(50, total_limit - offset)  # Limit per request, maximum 50
            tracks = sp.artist_top_tracks(artist_id, country=country_code)

            for track in tracks['tracks']:
                track_id = track['id']
                if track_id not in unique_song_ids:
                    unique_song_ids.add(track_id)
                    top_tracks.append(track)

                if len(unique_song_ids) >= total_limit:
                    break

            offset += limit

            if not tracks['tracks'] or len(unique_song_ids) >= total_limit:
                break
        except Exception as e:
            print(f"Error for artist ID {artist_id}: {str(e)}")
            artists_with_errors.append(artist_id)
            break

    return top_tracks


# Usage
# top_tracks = get_top_tracks(artist_id, total_limit=100)
# Iterate through the artists and find their top tracks
for artist_name in artists_df['name']:
    print(f"Searching for top tracks by {artist_name}...")

    # Search for the artist
    results = sp.search(q=f'artist:"{artist_name}"', type='artist', limit=1)

    if results['artists']['items']:
        artist = results['artists']['items'][0]
        artist_id = artist['id']
        top_tracks = get_top_tracks(artist_id)
        for track_id in top_tracks:
            try:
                # Extract track information
                track_info = sp.track(track_id['id'])  # Corrected the variable to track_id
                audio_features = sp.audio_features([track_id['id']])[0]  # Corrected the variable to track_id
                data = {
                    'tempo': audio_features['tempo'],
                    'valence': audio_features['valence'],
                    'speechiness': audio_features['speechiness'],
                    'loudness': audio_features['loudness'],
                    'liveness': audio_features['liveness'],
                    'instrumentalness': audio_features['instrumentalness'],
                    'energy': audio_features['energy'],
                    'duration_ms': audio_features['duration_ms'],
                    'danceability': audio_features['danceability'],
                    'acousticness': audio_features['acousticness'],
                    'album': track_info['album']['name'],
                    'artist': track_info['artists'][0]['name'],
                    'name': track_info['name'],
                    'explicit': track_info['explicit'],
                    'genre': artist['genres'][0] if artist['genres'] else None
                }

                track_data_list.append(data)
            except Exception as e:
                print(f"Error for track ID {track_id['id']} for artist {artist_name}: {str(e)}")

# Create a Pandas DataFrame from the list of data dictionaries
df = pd.DataFrame(track_data_list)

# Print or save the DataFrame as needed
print(df)

# Print the artists with errors
print("Artists with Errors:", artists_with_errors)
