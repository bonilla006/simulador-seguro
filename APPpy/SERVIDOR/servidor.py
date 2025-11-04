from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token

@app.route('/')
def index():
    return render_template('index.html', num=None)