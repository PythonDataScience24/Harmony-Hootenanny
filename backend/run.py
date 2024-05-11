from flask_cors import CORS
from harmonyhootenanny import create_app, socketio

if __name__ == "__main__":
    app = create_app()
    CORS(app,resources={r"/*":{"origins":"*"}})
    socketio.run(app)