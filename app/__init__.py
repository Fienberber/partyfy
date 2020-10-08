#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

# Set app.config here
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/user.db'

from app import routes
