# extensions.py
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize Flask extensions
socketio = SocketIO()
db = SQLAlchemy()
login_manager = LoginManager()

