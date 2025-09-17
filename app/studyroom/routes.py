from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import studyroom_bp
from app.models import StudyRoom, Message
from app.extensions import db
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@studyroom_bp.route('/rooms')
@login_required
def room_list():
    rooms = StudyRoom.query.all()
    return render_template('rooms/list.html', rooms=rooms)


@studyroom_bp.route('/rooms/create', methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        name = request.form['name'] # get the value the user enters in the name field and store in name
        description = request.form['description']
        new_room = StudyRoom(name=name, description=description, host_id=current_user.id)
        db.session.add(new_room)
        db.session.commit()
        flash("Study room created!", "success")
        return redirect(url_for('studyroom.room_list'))
    return render_template('rooms/create.html')


@studyroom_bp.route('/rooms/<int:room_id>') # pass in the room_id number into the function. ex: 10
@login_required
def room_detail(room_id): # go into and find room id 10
    room = StudyRoom.query.get_or_404(room_id)
    return render_template('rooms/detail.html', room=room)


@studyroom_bp.route('/rooms/<int:room_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)

    if room.host_id != current_user.id:
        flash("You don't have permission to edit this room", "danger")
        return redirect(url_for('studyroom.room_list'))
    
    if request.method == 'POST': # if post method is called update name and description of room
        room.name = request.form['name']
        room.description = request.form['description']
        db.session.commit() # commit the changes so they are saved to the database
        flash("Room updated sucessfully", "success")
        return redirect(url_for('studyroom.room_detail', room_id=room.id))
    return render_template('rooms/edit.html', room=room)

@studyroom_bp.route('/rooms/<int:room_id>/delete', methods=['POST'])
@login_required
def delete_room(room_id):
    room = StudyRoom.query.get_or_404(room_id)

    if room.host_id != current_user.id:
        flash("You don't have permission to delete this room.", "danger")
        return redirect(url_for('studyroom.room_list'))
    
    db.session.delete(room)
    db.session.commit()
    flash("Room deleted successfully.", "info")
    return redirect(url_for('studyroom.room_list'))

@studyroom_bp.route('/rooms/<int:room_id>/chat')
@login_required
def chat(room_id):
    room = StudyRoom.query.get_or_404(room_id)
    messages = Message.query.filter_by(room_id=room.id).order_by(Message.timestamp.asc()).all()
    return render_template('rooms/chat.html', room=room, messages=messages)


@studyroom_bp.route('/assistant', methods=['GET', 'POST'])
@login_required
def ai_assistant():
    response = None
    if request.method == 'POST':
        message = request.form.get('message')  
        if not message:
            return render_template('rooms/assistant.html', response="⚠️ Message is required.")
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": message}
            ]
        )
        response = completion.choices[0].message.content

    return render_template('rooms/assistant.html', response=response)