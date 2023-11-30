from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


class ClusteringAlgorithm:
    # Reducing the num of columns of the dataset using PCA (13 -> 2)
    def pca(self, df):
        # Extract and store id, popularity and year values
        song_id = df['id'].values
        popularity = df['popularity'].values
        name = df['name'].values

        # Apply PCA on Energy Features
        energy_columns = ['acousticness', 'danceability', 'energy', 'explicit', 'liveness', 'tempo']
        pca_energy = PCA(n_components=1)
        pca_energy_result = pca_energy.fit_transform(df[energy_columns])

        # Apply PCA on Mood Features
        mood_columns = ['instrumentalness', 'key', 'loudness', 'mode', 'speechiness', 'valence']
        pca_mood = PCA(n_components=1)
        pca_mood_result = pca_mood.fit_transform(df[mood_columns])

        # Combine PCA results with original track_uri values
        df_energy_mood_pca = pd.DataFrame(data={'song_id': song_id,
                                                'popularity': popularity,
                                                'name': name,
                                                'PCA_Energy': pca_energy_result[:, 0],
                                                'PCA_Mood': pca_mood_result[:, 0]})
        return df_energy_mood_pca

    # Using elbow method to see how many clusters works best
    def kmeans_cluster_tuning(self, data):
        # Taking random sample as dataset is too large
        random_sample = data.sample(frac=0.03, replace=False, random_state=1)

        # elbow method for identifying optimal cluster
        possible_clusters = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
        inertia = []
        for num_clusters in possible_clusters:
            kmeans = KMeans(n_clusters=num_clusters, random_state=42)
            kmeans.fit(random_sample)
            inertia._append(kmeans.inertia_)
        differences = [inertia[i + 1] - inertia[i] for i in range(len(inertia) - 1)]
        min_drop_index = differences.index(np.median(differences))
        self.plot_elbow(possible_clusters, inertia)
        return possible_clusters[min_drop_index]

    def plot_elbow(self, possible_clusters, inertia):
        # plot elbow score by cluster
        plt.plot(possible_clusters, inertia, marker='o')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Inertia (Within-Cluster Sum of Squares)')
        plt.title('Elbow Method for Optimal Number of Clusters')
        plt.show()

    # visualizations
    def visualizing_results(self, data, kmeans):
        # Plot the predicted clusters
        plt.scatter(data[:, 3], data[:, 4], c=kmeans.labels_, cmap='viridis', marker='o', edgecolor='k', alpha=0.5,
                    label='Predicted Clusters')
        plt.title('Song Attribute Clusters')
        plt.xlabel('PCA_Energy')
        plt.ylabel('PCA_Mood')
        plt.show()

    def run_clustering_algorithm(self):
        start_time = datetime.now()
        print("1. Reading Songs DataSet")
        df_raw = pd.read_csv('../test/resources/spotify_song_data.csv')
        df_raw = df_raw.drop_duplicates(subset=['name'])
        df_raw = df_raw.drop_duplicates(subset=['id'])
        row, col = df_raw.shape
        print(f'There are {row} rows and {col} columns')

        print("2. Reducing via PCA")
        pca_result = self.pca(df_raw)

        print("3. HyperTuning the Parameter for KMeans")
        optimum_num_clusters = self.kmeans_cluster_tuning(pca_result[['PCA_Energy', 'PCA_Mood']])
        # optimum_num_clusters=100
        print("optimum num of clusters =", optimum_num_clusters)

        print("4. Starting K-means clustering")
        song_id = pca_result['song_id'].values
        popularity = pca_result['popularity'].values
        name = pca_result['name'].values
        kmeans_energy = KMeans(n_clusters=optimum_num_clusters, random_state=42)
        kmeans_energy.fit(pca_result[['PCA_Energy']])
        kmeans_mood = KMeans(n_clusters=optimum_num_clusters, random_state=42)
        kmeans_mood.fit(pca_result[['PCA_Mood']])
        kmeans_cluster_df = pd.DataFrame(data={'song_id': song_id,
                                               'popularity': popularity,
                                               'name': name,
                                               'energy_cluster': kmeans_energy.labels_,
                                               'mood_cluster': kmeans_mood.labels_
                                               })
        clustered_songs_path = '../test/resources/spotify_song_data_clustered.csv'
        kmeans_cluster_df.to_csv(clustered_songs_path, index=False)
        print("5. Visualizing data")
        self.visualizing_results(pca_result.to_numpy(), kmeans_energy)
        end_time = datetime.now()
        elapsed_time = end_time - start_time
        print(f"Elapsed Time: {elapsed_time}")
        return clustered_songs_path

    def derive_energy_mood_cluster(self, clustered_songs, input_song):
        clustered_songs_data = clustered_songs[
            clustered_songs['name'].str.contains(input_song, case=False)].sort_values(by='popularity',
                                                                                      ascending=False).head(1)
        if not clustered_songs_data.empty:
            energy_cluster = clustered_songs_data['energy_cluster'].iloc[0]
            mood_cluster = clustered_songs_data['mood_cluster'].iloc[0]
        else:
            # assign a cluster outside range to return no song found when song matching keyword not found
            energy_cluster = 110
            mood_cluster = 110
        return energy_cluster, mood_cluster

    def get_song_clusters(self, energy, mood, input_song):
        clustered_songs_path = '../test/resources/spotify_song_data_clustered.csv'
        clustered_songs = pd.read_csv(clustered_songs_path)
        if input_song is not None:
            energy, mood = self.derive_energy_mood_cluster(clustered_songs, input_song)
        energy_condition = clustered_songs['energy_cluster'] == energy
        mood_condition = clustered_songs['mood_cluster'] == mood
        filtered_songs = clustered_songs[energy_condition & mood_condition].sort_values(by='popularity',
                                                                                        ascending=False)
        if filtered_songs.empty or len(filtered_songs) < 5:
            energy_min = energy - 5
            energy_max = energy + 5
            mood_min = mood - 5
            mood_max = mood + 5
            energy_condition_min = clustered_songs['energy_cluster'] > energy_min
            energy_condition_max = clustered_songs['energy_cluster'] <= energy_max
            mood_condition_min = clustered_songs['mood_cluster'] > mood_min
            mood_condition_max = clustered_songs['mood_cluster'] <= mood_max
            filtered_songs_add = clustered_songs[energy_condition_min & energy_condition_max
                                                 & mood_condition_min & mood_condition_max].sort_values(by='popularity',
                                                                                                        ascending=False)
            filtered_songs_add = filtered_songs_add[~energy_condition & ~mood_condition]
            filtered_songs = filtered_songs._append(filtered_songs_add)
        if input_song is not None:
            popular_songs = filtered_songs[~filtered_songs['name'].str.contains(input_song, case=False)].head(5)
            if popular_songs.empty or len(popular_songs) < 5:
                popular_songs_add = filtered_songs[~filtered_songs['name'].str.contains(input_song, case=False)]
                popular_songs_add = popular_songs_add.head(5 - len(popular_songs))
                popular_songs = popular_songs._append(popular_songs_add)
        else:
            popular_songs = filtered_songs.head(5)
        return popular_songs
