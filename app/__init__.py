#!/usr/bin/env python3

from flask import Flask
from .secrets import SECRET_KEY

app = Flask(__name__)

# Set app.config here
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Get rid of the warning
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/user.db'

from app import routes
