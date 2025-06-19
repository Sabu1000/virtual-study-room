from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app.extensions import socketio, db
from app.models import Message

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('message', {
        'user': 'System',
        'text': f'{current_user.username} has joined the room.'
    }, room=room)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    text = data['text']
    user_id = current_user.id

    # save to DB
    message = Message(room_id=room, user_id=user_id, content=text)
    db.session.add(message)
    db.session.commit()

    emit('message', {
        'user': current_user.username,
        'text': text
    }, room=room)

