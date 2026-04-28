from flask import Blueprint, render_template
from app.models.itinerary import Itinerary

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁 (行程列表)"""
    itineraries = Itinerary.get_all()
    return render_template('index.html', itineraries=itineraries)
