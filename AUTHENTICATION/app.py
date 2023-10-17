from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key="secret_key"
app.config["MONGO_URI"]="mongodb+srv://mehtadev92:dev123@cluster0.k7tyds0.mongodb.net/auth?retryWrites=true&w=majority"
mongo = PyMongo(app)