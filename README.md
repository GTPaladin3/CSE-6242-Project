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
unzip team100final.zip
cd CSE-6242-Project\src\main\
Install below python packages
pip install pytest
pip install numpy matplotlib scikit-learn
pip install streamlit
pip install spotipy

**EXECUTION:**
cd src\main\
streamlit run App.py
Click to refresh emotion/mood clusters using spotify song dataset --> This option will build emotion and mood clusters for spotify song data set under CSE-6242-Project\src\test\resources\spotify_song_data.csv. Ouput will be stored in CSE-6242-Project\src\test\resources\spotify_song_data_clustered.csv
Enter a song you like or use the mood selector bar on left:
Enter song in the text box and click on recommend songs, this option will provide five recommendations based on entered keyword
Clear keyword in the text box, use the sliders to select energy/mood and click on recommend songs, this option will provide three recommendations based on energy/mood selected

**DEMO VIDEO: **

