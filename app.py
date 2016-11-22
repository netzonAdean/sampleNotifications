from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import random


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:samatosa@localhost/notifix1"

db = SQLAlchemy(app)



# ----------------- SIMPLE SqlAlchemy Model ------------------------
class simple_list(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, username, email):
		self.username = username
		self.email = email

	def __repr__(self):
		return "User: %s  |  Email: %s" % (self.username, self.email)


# ----------------- ONE to MANY Relationship -----------------------
class Person(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	addresses = db.relationship("Address", backref="person", lazy="dynamic")

class Address(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(50))
	person_id = db.Column(db.Integer, db.ForeignKey("person.id"))


#class Person(db.Model):
#	id =  db.Column(db.Integer, primary_key=True)
#	name = db.Column(db.String(50))
#	addresses = db.relationship("Address", backref = db.backref("person", lazy="joined"),  lazy="dynamic")



# ---------------- MANY to MANY Relations ---------------------------
tags = db.Table("tags", db.Column("tag_id", db.Integer, db.ForeignKey("tag.id")), db.Column("page_id", db.Integer, db.ForeignKey("page.id")))

class Page(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tags = db.relationship("Tag", secondary=tags, backref=db.backref("pages", lazy="dynamic"))

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
#--------------------------------------------------------------------



#db.create_all()


#CRUD functions =====================================================

#Create new data sample on 'simple_list'
simple_data = simple_list(str(random.random()), str(random.random()) + "@gmail.com");
db.session.add(simple_data)
db.session.commit()

print(simple_list.query.all())

Person.query.join(Address).all()

