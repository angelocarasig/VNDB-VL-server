from audioop import cross
from flask import Blueprint, jsonify, request, send_from_directory
from .models import load_user_data
from api import cache

api = Blueprint('api', __name__)

@api.route("/get_user_data", methods=["POST"])
def get_user_data():
    userID = request.get_json()
    data = get_ulist(userID['userID'])
    return jsonify(data)

@cache.memoize(timeout=86400)       # Assume that it resets per day
def get_ulist(userID):
    user = load_user_data(userID)
    return user