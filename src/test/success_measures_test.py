import unittest

import pandas as pd

from src.main.ClusteringAlgorithm import ClusteringAlgorithm


class Tests(unittest.TestCase):  # creating the class
    def test_clustering_algorithm(self):
        # method that tests the count of clustered songs
        clustering_algorithm = ClusteringAlgorithm()
        clustered_song_path = clustering_algorithm.run_clustering_algorithm()
        clustered_songs = pd.read_csv(clustered_song_path)
        self.assertEqual(137013, len(clustered_songs))

    def test_cluster_assignment_by_energy_mood(self):
        # method that tests the count of clustered songs
        clustering_algorithm = ClusteringAlgorithm()
        energy = 0
        mood = 2
        energy_min = energy - 5
        energy_max = energy + 5
        mood_min = mood - 5
        mood_max = mood + 5
        identified_songs = clustering_algorithm.get_song_clusters(energy, mood, None)
        self.assertEqual(5, len(identified_songs))
        for index, row in identified_songs.iterrows():
            # validate if duplicate songs are not present
            self.assertEqual(len(identified_songs[identified_songs['name'] == row['name']]), 1)
            # validate if songs are in the cluster range of input energy and mood
            self.assertLessEqual(row['energy_cluster'], energy_max)
            self.assertGreater(row['energy_cluster'], energy_min)
            self.assertLessEqual(row['mood_cluster'], mood_max)
            self.assertGreater(row['mood_cluster'], mood_min)

    def test_cluster_assignment_by_name(self):
        # method that tests the count of clustered songs
        clustering_algorithm = ClusteringAlgorithm()
        clustered_songs_path = '../test/resources/spotify_song_data_clustered.csv'
        clustered_songs = pd.read_csv(clustered_songs_path)
        song_name = 'Shakira'
        energy, mood = clustering_algorithm.derive_energy_mood_cluster(clustered_songs, song_name)
        energy_min = energy - 5
        energy_max = energy + 5
        mood_min = mood - 5
        mood_max = mood + 5
        identified_songs = clustering_algorithm.get_song_clusters(None, None, 'Shakira')
        self.assertEqual(5, len(identified_songs))
        for index, row in identified_songs.iterrows():
            # validate if duplicate songs are not present
            self.assertEqual(len(identified_songs[identified_songs['name'] == row['name']]), 1)
            # validate if songs are in the cluster range of input song energy and mood
            self.assertLessEqual(row['energy_cluster'], energy_max)
            self.assertGreater(row['energy_cluster'], energy_min)
            self.assertLessEqual(row['mood_cluster'], mood_max)
            self.assertGreater(row['mood_cluster'], mood_min)

    def validate(a, b):  # defining the function to be tested
        return a * b


if __name__ == '__main__':
    unittest.main()
