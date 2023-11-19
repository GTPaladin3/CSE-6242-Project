import streamlit as st
import pydeck as pdk
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

def recommend_songs(input, x, y):
    return input


SPOTIPY_CLIENT_ID = '255ff85062be4aaaba1ec5fa597a8eea'
SPOTIPY_CLIENT_SECRET = '4b2241df02174c1eba41cc3293cd61f2'
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
# Create Spotify API client
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_song_info(song_names):
    # Search for a song
    song_data = []
    results = sp.search(q=song_names, type='track', limit=1)
    # Extract relevant information from the search results
    if results['tracks']['items']:
            track = results['tracks']['items'][0]
            title = track['name']
            artist = track['artists'][0]['name']
            album_cover_url = track['album']['images'][0]['url']
            song_data.append({'Title': title, 'Artist': artist, 'Album Cover': album_cover_url})
            return song_data


def main():

    st.title("Music Recommendation System")

    input_song = st.text_input("Enter a song you like:")
    title = None
    artist = None
    song_info = []
    # Mood selector graph
    st.sidebar.header("Mood Selector")

    # Initialize the button position in the middle
    x_axis = st.sidebar.slider("Energy (Relaxed to Energetic)", 0, 100, 50, key="x_axis")
    y_axis = st.sidebar.slider("Mood (Sad to Happy)", 0, 100, 50, key="y_axis")

    # Set the graph in the middle of the page
    st.sidebar.markdown('<style>div.Widget.row-widget.stRadio>div{flex-direction:row;}</style>', unsafe_allow_html=True)
    
    # Display the current button position
    #st.sidebar.write(f"Current Mood Position: Energy={x_axis}, Mood={y_axis}")

    # Button to trigger recommendation
    if st.button("Recommend Songs"):
        # Output recommendation based on user inputs
        st.write(f"Your selected mood coordinates: Energy: {x_axis}, Mood: {y_axis}")
        st.write(f"Input Song: {input_song}")

        # Call your recommendation function here and display the recommended songs
        recommended_songs = recommend_songs(input_song, x_axis, y_axis)
        #st.write("Recommended Songs:")
        if input_song:
            # Get song information from Spotify API
            song_info = get_song_info(f'"{input_song}"')
            if song_info:
                first_song_info = song_info[0]
                title = first_song_info['Title']
                
                # Display song information
                #st.write("Song Information:")
                #st.write(f"Title: {title}")
                #st.image(first_song_info['Album Cover'], caption=f"Album Cover: {first_song_info['Title']}", use_column_width=True)
                #st.write(f"Artist: {artist}")

                # Display album cover
                #st.image(album_cover_url, caption=f"Album Cover: {title}", use_column_width=True)
            else:
                st.warning("Song not found on Spotify. Please try another song.")
    df = pd.DataFrame(song_info)
    

    # Data table to display mood coordinates
    st.subheader("Recommended Songs")
    st.data_editor(df,
    column_config={
        "Title": "Song Title",
        "Artist": "Artist",
        "Album Cover": st.column_config.ImageColumn("Album Cover", help="Streamlit app preview screenshots")
    },
    hide_index=True,)


if __name__ == "__main__":
    main()