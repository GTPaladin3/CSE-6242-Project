# Instructions for Music Recommendation System

**DESCRIPTION :**
CSE-6242-Project has all the required components for clustering song data, a UI component that renders the song recommendation system, and clustered data for faster song recommendation rendering in UI. Please find below the brief description of each folder's content
1. src/.streamlit - UI Sytle Tags
2. src/main/App.py - UI Interface Code which allows user to enter energy and mood or enter a song and request recommendation. 
3. src/main/ClusteringAlgorithm.py - Clustering algorithm and filtering logic to identify song id's based on user provided energy and mood    cluster or based on input song's energy and mood cluster
4. src/main/Spotify_API_Demo.py - Spotify API code to extract song data
5. src/test/resources/spotify_song_data.csv - song data extracted using spotify api
6. src/test/resources/spotify_song_data_clustered.csv - song data clustered using k-means algorithm

**INSTALLATION:**
1. unzip team100final.zip
2. cd CSE-6242-Project\src\main\
3. pip install pytest
4. pip install pandas
5. pip install numpy matplotlib scikit-learn
6. pip install streamlit
7. pip install spotipy

**EXECUTION:**
1. cd src\main\
2. streamlit run App.py
3. Click to refresh emotion/mood clusters using spotify song dataset --> This option will build emotion and mood clusters for spotify song data set under CSE-6242-Project\src\test\resources\spotify_song_data.csv. Ouput will be stored in CSE-6242-Project\src\test\resources\spotify_song_data_clustered.csv
4. Enter a song you like or use the mood selector bar on left
5. Enter song (for example: Christmas) in the text box and click on recommend songs, this option will provide five recommendations based on entered keyword
6. Clear keyword in the text box, use the sliders to select energy/mood and click on recommend songs, this option will provide three recommendations based on energy/mood selected

**DEMO VIDEO: **

