from .models import *
from .views import *
from .controllers import *
from .main import *


import os

app = create_app()

# Secret key for sessions
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'devsecret')

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Optional environment settings
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = int(os.environ.get('FLASK_DEBUG', 0))



# from flask import Flask
# from .config import load_config
# from .models import db  
# from .views import apartment_views
# from sqlalchemy import event
# from sqlalchemy.engine import Engine
    
#     # Config settings here (replace with actual config or config object)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdb.sqlite3'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.secret_key = 'your-secret-key'

#     db.init_app(app)

#     # Register Blueprints
#     app.register_blueprint(apartment_views)

#     return app

# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()


