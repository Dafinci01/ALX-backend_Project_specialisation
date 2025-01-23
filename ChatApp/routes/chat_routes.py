from flask import Blueprint, app, render_template, request, jsonify
from flask_socketio import emit, disconnect
from flask_login import login_required, current_user
from models import ChatMessage
from app import socketio
from extensions import db
import random

chat_bp = Blueprint('chat', __name__)

# Store connected users (key: socket id, value: username and avatar)
users = {}

@chat_bp.route('/')
@login_required
def index():
    return render_template('index.html',conversations=conversatons, username=current_user.username, profile_picture="profile.jpg")

@socketio.on("connect")
def handle_connect():
    if current_user.is_authenticated:
        username = current_user.username
        gender = random.choice(["boy", "girl"])
        avatar_url = f"https://avatar.iran.liara.run/public/{gender}?username={username}"
        users[request.sid] = {"username": username, "avatar": avatar_url}
        emit("user_joined", {"username": username, "avatar": avatar_url}, broadcast=True)
        emit("set_username", {"username": username})
    else:
        disconnect()

@socketio.on("disconnect")
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit("user_left", {"username": user["username"]}, broadcast=True)

@socketio.on("send_message")
def handle_message(data):
    user = users.get(request.sid)
    if user:
        # Save the message to the database
        new_message = ChatMessage(
            sender=user["username"],
            avatar=user["avatar"],
            message=data["message"]
        )
        db.session.add(new_message)
        db.session.commit()

        # Emit the new message to all connected clients
        emit("new_message", {
            "username": user["username"],
            "avatar": user["avatar"],
            "message": data["message"]
        }, broadcast=True)

@socketio.on("update_username")
def handle_update_username(data):
    user = users.get(request.sid)
    if user:
        old_username = user["username"]
        new_username = data["username"]
        user["username"] = new_username

        emit("username_updated", {
            "old_username": old_username,
            "new_username": new_username
        }, broadcast=True)

@chat_bp.route("/chat_history")
def chat_history():
    messages = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
    history = [
        {
            "username": message.sender,
            "avatar": message.avatar,
            "message": message.message,
            "timestamp": message.timestamp.isoformat()
        }
        for message in messages
    ]
    return jsonify(history)

