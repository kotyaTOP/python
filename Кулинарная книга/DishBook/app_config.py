from flask import Flask
from flask_sqlalchemy import SQLAlchemy


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:301098@localhost/mydb?auth_plugin=mysql_native_password"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config())
mydb = SQLAlchemy(app)
