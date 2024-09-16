from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify 
from dotenv import load_dotenv
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

load_dotenv()

app = Flask(__name__)
db_url = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@localhost/{os.getenv("DB_NAME")}'
app.secret_key = os.getenv("SQLALCHEMY_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['JWT_SECRET_KEY'] = os.getenv("SQLALCHEMY_KEY") 

db = SQLAlchemy(app)
jwt = JWTManager(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    cell = db.Column(db.String(12), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    Date_Created = db.Column(db.DateTime(), default= datetime.now, nullable = False)
    Date_Updated = db.Column(db.DateTime(), default= datetime.now, onupdate= datetime.now, nullable = False)

    def __repr__(self):
        return f'<User {self.name}>'