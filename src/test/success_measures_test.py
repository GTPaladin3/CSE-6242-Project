import unittest

from src.main.ClusteringAlgorithm import ClusteringAlgorithm


def prod(a, b):  # defining the function to be tested
    return a * b


class Tests(unittest.TestCase):  # creating the class
    def test(self):  # method that test the function
        # test = Spotify_API_Demo.get_song_by_mood("test")
        clustering_algorithm = ClusteringAlgorithm()
        filtered_songs = clustering_algorithm.run_clustering_algorithm()
        # testing by calling the function and passing the predicted result


if __name__ == '__main__':
    unittest.main()