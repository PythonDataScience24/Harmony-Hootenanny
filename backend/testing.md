# Testing the add_song_to_db Function

## Description

The add_song_to_db function is responsible for adding a new song to the database. It accepts the following parameters:

title (str): The title of the song.
artist (str): The artist of the song.
duration (int): The duration of the song in seconds.
src (str): The source file of the song (e.g., file path).

## Unexpected results

The function might produce unexpected results under certain conditions:

- Adding a song with missing parameters.
- Adding a song with single string parameter.
- Adding a song with single int parameter.
- Adding a song with single dictionary parameter.

Calling the function under any of these conditions throws a TypeError.

## How We Tested It

### test_add_song_to_db

- Setup: The test ensures the songs table is empty before adding a new song.
- Action: Adds a song with specified parameters and retrieves it from the database.
- Verification: Checks if the song was added correctly by verifying each field.

### test_add_song_without_input

- Setup: Calls the add_song_to_db function without any input parameters.
- Action: Tries calling the function without parameters.
- Verification: Ensures a TypeError is raised due to missing required positional arguments.

### test_add_song_single_string_input

- Setup: Calls the add_song_to_db function with a single string input parameter.
- Action: Tries calling the function with a single string input.
- Verification: Ensures a TypeError is raised due to missing required positional arguments.

### test_add_song_single_int_input

- Setup: Calls the add_song_to_db function with a single integer input parameter.
- Action: Tries calling the function with a single integer input.
- Verification: Ensures a TypeError is raised due to missing required positional arguments.

### test_add_song_single_dict_input

- Setup: Calls the add_song_to_db function with a single dictionary input parameter.
- Action: Tries calling the function with a single dictionary input.
- Verification: Ensures a TypeError is raised due to missing required positional arguments.
