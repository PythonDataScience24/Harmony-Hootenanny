# Harmony Hootenanny

In **Harmony Hootenanny** we create an easy joint listening party for users to enjoy their music together. We created this project for the course “Programming for Data Science” at the University of Bern.
What makes our project exceptional is the easy accessibility to listen to the same music at the same time as your friends.

## How to get started:

### Prerequisites

Ensure you have Python, pip, Node.js, and npm installed on your machine. These are essential to run the backend and frontend of our project.

### Backend Setup

After cloning the repository change into the backend folder of this project:

```
cd backend
```

For our application we need several packages which can be installed using the `requirements.txt` file:

```
pip install -r requirements.txt
```

After the packages are installed you can start the backend server using the following command:

```Bash
py run.py # windows
python3 run.py # linux
```

### Frontend Setup

In another terminal change into the frontend folder:

```
cd frontend
```

Install the required node modules:

```
npm install
```

After the packages are installed you can start the frontend server using the following command:

```
npm start
```

Now the frontend will run at `http://localhost:3000/` in your browser.

# Roadmap

Our mission with **Harmony Hootenanny** is to create a web mp3 player that allows multiple users to listen to the same song at the same time with as few hurdles as possible.

## Milestones

- Initial Setup (02.05.2024)
  To start such a project we have to initialize a front- & backend in order to create the basis for storing and replaying audio files on a webclient. React will be used in the frontend and a Flask server in the backend. To store data on Sessions we will use any SQL (relational) database.
- Listening Parties (16.05.2024)
  For our project to be more than a reskin of Spotify's web client we want the main purpose of our site to be Listening Parties where people can tune in remotely to the same broadcast, just like real life radio channels but digital and not restricted by the government. To make it more enjoyable, members of a party will be able to queue up songs in that room.
- Data Analysis (23.05.2024)
  To fit this course's agenda more firmly we want to analyze data gathered from users regarding sessions like songs played most often, top artists and hours listened in and display it in a publicly available dashboard.

Tasks per milestone: read text again

## Current changes

Since the first milestone we implemented several new features:

- **Dashboard**: We added a dashboard page where you can see some (mostly mocked) user statistics. Here we display information like number of listeners in a room, top users who added songs to the queue as well as information about each room and more.
- **Song Scheduler**: We finished the implementation of the SongScheduler which now pauses and skip songs for all users in the room. Also after a song is finished it will automatically play the next song from the queue.
- **Youtube Downloader**: Using the searchbar you can now also add a link to a song on YouTube which will be downloaded and added to the database as well as the song queue. We also added a tooltip explaining how it works.
- **Queue integration into Websocket**: We changed the logic from an API endpoint for the queue in the routes file into an event in the websocket.
- **Mocked Database**: We created a script to populate the database with mock information so we have more data to analyze. These songs are **not** download. Therefore you can **not** play these songs although they appear in the search bar and will be added to the queue.

## Events

In-person presentation: 30. May 2024
