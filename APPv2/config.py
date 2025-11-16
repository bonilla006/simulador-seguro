from dotenv import load_dotenv
import os
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

if os.getenv('DEVENV'): 
    database = f'sqlite:///{os.path.join(basedir, "app.db")}'
else:
    database = os.getenv('DATABASE')

class Config:
    SQLALCHEMY_DATABASE_URI = database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
