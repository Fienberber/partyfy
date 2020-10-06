#!/usr/bin/env python3

from flask import Flask

app = Flask(__name__)

# Set app.config here

from app import routes
