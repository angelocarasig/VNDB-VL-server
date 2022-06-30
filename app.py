from audioop import cross
from functools import cache
from flask import Flask, jsonify, request
from flask_caching import Cache
from models import load_user_data
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cache = Cache()

app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)
CORS(app)
@app.route("/get_user_data", methods=["POST"])
@cross_origin()
def get_user_data():
    userID = request.get_json()
    data = get_ulist(userID['userID'])
    return jsonify(data)

@cache.memoize(timeout=86400)       # Assume that it resets per day
def get_ulist(userID):
    user = load_user_data(userID)
    return user