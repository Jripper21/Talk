# server.py
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    socketio.emit('message', {'msg': f'{username} has joined the room.'}, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.emit('message', {'msg': f'{username} has left the room.'}, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    socketio.emit('message', {'msg': data['msg']}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
