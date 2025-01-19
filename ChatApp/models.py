from flask_login import UserMixin
from extensions import db
from datetime import datetime, timezone

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"

class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    avatar = db.Column(db.String(255))  # Add avatar field
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def __init__(self, sender, message, avatar=None):
        self.sender = sender
        self.message = message
        self.avatar = avatar
