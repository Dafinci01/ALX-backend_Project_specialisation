from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from extensions import db 
import random

ai_bp = Blueprint('ai-route', __name__)

@ai_bp.route('/chat-feed')
@login_required
def index():
    """ 
    index route to display the ai inyterface 
    """
    try:
        #Fetch ai data from database api 
        