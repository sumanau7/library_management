from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

# when we initialize our app we also need to initialize our database
db = SQLAlchemy(app)

from app import views, models

