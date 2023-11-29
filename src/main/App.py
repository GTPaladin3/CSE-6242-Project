import pandas as pd
import spotipy
import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials

from ClusteringAlgorithm import ClusteringAlgorithm


def recommend_songs(energy, mood):
    clustering_algorithm = ClusteringAlgorithm()
    filtered_songs = clustering_algorithm.get_song_clusters(energy, mood)
    return filtered_songs


def refresh_song_cluster():
    clustering_algorithm = ClusteringAlgorithm()
    filtered_songs = clustering_algorithm.run_clustering_algorithm()


SPOTIPY_CLIENT_ID = '255ff85062be4aaaba1ec5fa597a8eea'
SPOTIPY_CLIENT_SECRET = '4b2241df02174c1eba41cc3293cd61f2'
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
# Create Spotify API client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
#Get data in CSV format
raw_data = pd.read_csv('../test/resources/spotify_song_data_clusters_joined.csv')

def get_song_info(song_names):
    # Search for a song by name
    song_data = []
    results = sp.search(q=song_names, type='track', limit=5)
    # Extract relevant information from the search results
    if results['tracks']['items']:
        print(len(results['tracks']['items']))
        for i in range(0, len(results['tracks']['items'])):
            track = results['tracks']['items'][i]
            title = track['name']
            artist = track['artists'][0]['name']
            album_cover_url = track['album']['images'][0]['url']
            song_data.append({'Title': title, 'Artist': artist, 'Album Cover': album_cover_url})
        return song_data


def get_song_info_track_name(recommended_songs):
    # Search for a song by track
    song_data = []
    for index, row in recommended_songs.iterrows():
        track = sp.track(row['song_id'])
        # Extract relevant information from the search results
        if track:
            title = track['name']
            artist = track['artists'][0]['name']
            album_cover_url = track['album']['images'][0]['url']
            song_data.append({'Title': title, 'Artist': artist, 'Album Cover': album_cover_url})
    return song_data


def main():
 
    st.title("Music Recommendation System")
    input_song = st.text_input("Enter a Song Here That Matches Your Mood!")
    song_info = []
    # Mood selector graph
    st.sidebar.header("Mood Selector", divider= "green")

    # Initialize the button position in the middle
    x_axis = st.sidebar.slider("Energy (Relaxed to Energetic)", 0, 100, 50, key="x_axis")
    y_axis = st.sidebar.slider("Mood (Sad to Happy)", 0, 100, 50, key="y_axis")

    st.sidebar.subheader("How To", divider= "green")
    with st.sidebar.expander("Click to Expand"):
        st.text("Input a song that matches your\nmood or use our mood selector \nabove! The mood selector is\nonly used when a song is not\ngiven. If you do choose to\nenter a song, remember that\nspelling matters. ")
    # Button to trigger recommendation
    if st.button("Recommend Songs"):
        # if input song is present use that or else call your recommendation function
        # here and display the recommended songs
        if input_song:
            st.write(f"Recommendation Based on Input Song: {input_song}")
            # Get song information from Spotify API
            filtered_data = raw_data[raw_data['name'] == input_song]
            if not filtered_data.empty:
                ordered_data = filtered_data.sort_values(by='popularity', ascending=False)
                mood_cluster = ordered_data['mood_cluster'].iloc[0]
                energy_cluster = ordered_data['energy_cluster'].iloc[0]
                recommended_songs = recommend_songs(energy_cluster, mood_cluster)
            # Get song information from Spotify API
                song_info = get_song_info_track_name(recommended_songs)
            else:
                st.warning("Song not found on Spotify. Please try another song.")
        else:
            st.write(f"Your Selected Mood Coordinates: Energy: {x_axis}, Mood: {y_axis}")
            recommended_songs = recommend_songs(x_axis, y_axis)
            # Get song information from Spotify API
            song_info = get_song_info_track_name(recommended_songs)
    df = pd.DataFrame(song_info)
    
    # Data table to display mood coordinates
    st.subheader("Recommended Songs")
    if not df.empty:
    # Display the data table
        st.data_editor(df,
                   column_config={
                       "Title": "Song Title",
                       "Artist": "Artist",
                       "Album Cover": st.column_config.ImageColumn("Album Cover",
                                                                   help="Streamlit app preview screenshots")
                   },
                   hide_index=True)
    else:
    # Display a message when the DataFrame is empty
        st.warning("No data to display.")

    # Button to trigger recommendation
    #if st.button("Click to Refresh Mood Clusters"):
    #    refresh_song_cluster()
    #    st.info("Song Cluster Refresh Completed")


if __name__ == "__main__":
    main()
