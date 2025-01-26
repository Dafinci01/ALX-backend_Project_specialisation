from flask_login import UserMixin
from extensions import db
from datetime import datetime, timezone



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    #email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)  # Ensure only one password column
    profile_image_url = db.Column(db.String(300), nullable=True)  # Optional profile image URL

    def __repr__(self):
        return f"<User {self.username}>"


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(255), nullable=True)  # Avatar is optional
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # No need for __init__ unless custom initialization is needed.
    def __repr__(self):
        return f"<ChatMessage from {self.sender} at {self.timestamp}>"
