"""Main function of our server, run this file to start the backend"""
from flask_cors import CORS
from database import init_db
from harmonyhootenanny import create_app, socketio

if __name__ == "__main__":
    init_db()
    app = create_app()
    CORS(app,resources={r"/*":{"origins":"*"}})
    socketio.run(app)
