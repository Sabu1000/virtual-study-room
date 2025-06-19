from app import create_app
from app.extensions import socketio

app = create_app()

if __name__ == "__main__": # check if script is being run directly rather than being imported by another module
    socketio.run(app, debug=True) # socketio allows real-time, bidirectional communication between clients. similar to app.run()