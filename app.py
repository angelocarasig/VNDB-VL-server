from audioop import cross
from functools import cache
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors import CORS, cross_origin
from models import load_user_data

app = Flask(__name__)
CORS(app)
cache = Cache()

app.config['CACHE_TYPE'] = 'simple'
cache.init_app(app)

@app.route("/")
@cross_origin()
def home():
    return "<h1>test server</h1>"

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

if __name__ == "__main__":
    app.run(debug=True)