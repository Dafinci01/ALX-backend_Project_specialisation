import os
from flask import Blueprint, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_socketio import emit, disconnect
from flask_login import login_required, current_user
from extensions import db
import random

upload_bp = Blueprint('upload', __name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # Secure the filename
            file.save(os.path.join(UPLOAD_FOLDER, filename))  # Save the file

            return redirect(url_for('upload.uploaded_file', filename=filename))  # Redirect to display the image

    return render_template('upload.html')  # Show the upload form

@upload_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return render_template('profile.html', filename=filename)  # Show the uploaded image
