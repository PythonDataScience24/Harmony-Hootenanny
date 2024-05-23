# test_add_song_to_db.py

import unittest
import sqlite3
import os
from database import add_song_to_db, get_db_connection

class TestAddSongToDb(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Create a temporary database for testing """
        cls.test_db = "database.db"
        with open('schema.sql', 'r') as schema_file:
            schema = schema_file.read()
        with sqlite3.connect(cls.test_db) as conn:
            conn.executescript(schema)

    @classmethod
    def tearDownClass(cls):
        """ Remove the temporary database after tests """
        os.remove(cls.test_db)

    def setUp(self):
        """ Override get_db_connection to use the test database """
        global get_db_connection
        self.original_get_db_connection = get_db_connection
        get_db_connection = self.get_test_db_connection

    def tearDown(self):
        """ Restore the original get_db_connection function """
        global get_db_connection
        get_db_connection = self.original_get_db_connection

    def get_test_db_connection(self):
        """ Helper function to return a connection to the test database """
        conn = sqlite3.connect(self.test_db)
        conn.row_factory = sqlite3.Row
        return conn

    def test_add_song_to_db(self):
        """ Test adding a song to the database """
        # Ensure the table is empty before the test
        with get_db_connection() as conn:
            conn.cursor().execute("DELETE FROM songs")
            conn.commit()

        # Add the song
        add_song_to_db("Test Song", "Test Artist", 300, "test.mp3")

        # Retrieve the song from the database
        with get_db_connection() as conn:
            song = conn.cursor().execute("SELECT * FROM songs WHERE title = 'Test Song'").fetchone()

        # Check if the song was added correctly
        self.assertIsNotNone(song, "The song was not added to the database.")
        self.assertEqual(song["title"], "Test Song")
        self.assertEqual(song["artist"], "Test Artist")
        self.assertEqual(song["duration"], 300)
        self.assertEqual(song["src"], "test.mp3")

    def test_add_song_without_input(self):
        """ Test adding a song without any input parameters """
        with self.assertRaises(TypeError):
            add_song_to_db()

    def test_add_song_single_string_input(self):
        """ Test adding a song wit a single string input parameters """
        with self.assertRaises(TypeError):
            add_song_to_db("Test")

    def test_add_song_single_int_input(self):
        """ Test adding a song wit a single int input parameters """
        with self.assertRaises(TypeError):
            add_song_to_db(5)

    def test_add_song_single_dict_input(self):
        """ Test adding a song wit a single dict input parameters """
        with self.assertRaises(TypeError):
            add_song_to_db({1})

if __name__ == "__main__":
    unittest.main()
