import unittest

from src.main import Spotify_API_Demo


def prod(a, b):  # defining the function to be tested
    return a * b


class Tests(unittest.TestCase):  # creating the class
    def test(self):  # method that test the function
        test = Spotify_API_Demo.get_song_by_mood("test")
        self.assertEqual(prod(4, -2), 8)  # testing by calling the function and passing the predicted result


if __name__ == '__main__':
    unittest.main()