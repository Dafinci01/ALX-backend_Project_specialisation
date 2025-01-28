from flask import Blueprint, render_template, request, jsonify, current_app
from flask_socketio import emit, disconnect
from flask_login import  login_required, current_user
from models import ChatMessage
from extensions import db
from extensions import socketio
import random

chat_bp = Blueprint('chat', __name__)

# Store connected users (key: socket id, value: username and avatar)
users = {}


@chat_bp.route('/chat-feed')
@login_required
def index():
    """
    Index route to display the chat interface.
    """
    try:
        # Fetch conversation data from the database
        conversation = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
        # Render the template with conversation data
        return render_template(
            'index.html',
            conversation=conversation or [],
            username=current_user.username or 'Guest',
            profile_image_url=current_user.profile_image_url or 'default-profile.jpg'  # Replace with dynamic data if available
        )
    except Exception as e:
        current_app.logger.error(f"Error in index route: {e}")
        return "An error occurred", 500

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
    """
    Route to fetch the chat history.
    """
    try:
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
    except Exception as e:
        current_app.logger.error(f"Error fetching chat history: {e}")
        return "An error occurred", 500

@chat_bp.route("/conversation-content")
@login_required
def conversation():
    """
    Route to fetch or initialize conversation data.
    """
    try:
        # Fetch conversation data from the database
        conversation = ChatMessage.query.order_by(ChatMessage.timestamp.asc()).all()
        return jsonify([message.to_dict() for message in conversation])  # Assuming to_dict() is implemented
    except Exception as e:
        current_app.logger.error(f"Error fetching conversation: {e}")
        return "An error occurred", 500

@chat_bp.route("/chat-feed")
@login_required
def chat_feed():
    """
    Route to fetch chat feed data.
    """
    try:
        messages = ChatMessage.query.order_by(ChatMessage.timestamp.desc()).limit(20).all()
        feed = [
            {
                "username": message.sender,
                "avatar": message.avatar,
                "message": message.message,
                "timestamp": message.timestamp.isoformat()
            }
            for message in messages
        ]
        return jsonify(feed)
    except Exception as e:
        current_app.logger.error(f"Error fetching chat feed: {e}")
        return "An error occurred", 500
