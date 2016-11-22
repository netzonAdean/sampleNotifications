from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:samatosa@localhost/notifix3"

db = SQLAlchemy(app)
