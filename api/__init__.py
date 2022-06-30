from functools import cache
from flask import Flask, send_from_directory
from flask_caching import Cache
from vndb_thigh_highs import VNDB


vndb = VNDB()

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = 'simple'
    cache.init_app(app)

    from .views import api
    app.register_blueprint(api)

    return app

