from audioop import cross
from flask import Blueprint, jsonify, request, send_from_directory
from .models import load_user_data
from api import cache
from flask_cors import CORS, cross_origin

api = Blueprint('api', __name__, static_folder="../../client/build", static_url_path="/")
cors = CORS(api)

@api.route("/get_user_data", methods=["POST"])
@cross_origin()
def get_user_data():
    userID = request.get_json()
    data = get_ulist(userID['userID'])
    return jsonify(data)

@cache.memoize(timeout=86400)       # Assume that it resets per day
def get_ulist(userID):
    user = load_user_data(userID)
    return user

@api.route("/")
@cross_origin()
def serve():
    return send_from_directory(api.static_folder, "index.html")