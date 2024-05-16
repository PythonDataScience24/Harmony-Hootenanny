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

- **Login**: We added user authentication to our app, so each user must be logged in to be able to join one of the rooms. This authentication will be used to identify and track the user. This is also preparation for the next milestone, where we will focus on tracking and visualizing user data.
- **Websockets**: We implemented websocket functionality, so users can now join rooms. When entering a room, the user will retrieve the song queue and the current playing song from the database. Also all other participants in that room are visible and joining/leaving is updated in real time. The only missing part here is that currently, the logic for tracking when a song finishes is not fully implemented yet and therefore cannot play the next song. In our test data, it is specified that the song started playing on May 16 at 12:34, and since this time has passed, the song will be at 2:44 and not start at 0:00. Additionally, if one user presses pause, it will not pause for all users in the current room.

## Events

In-person presentation: 30. May 2024
