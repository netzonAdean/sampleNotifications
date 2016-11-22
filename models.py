#from flask import Flask, jsonify
#from flask_sqlalchemy import SQLAlchemy

from flask import jsonify
from __init__ import app, db

#app = Flask(__name__)
#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:samatosa@localhost/notifix2"

#db = SQLAlchemy(app)

#----------------------------------------------------------------

class notificationheaders(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	notification_uuid = db.Column(db.String(20), unique=True)
	user_uuid = db.Column(db.String(20))
	company_uuid = db.Column(db.String(20))
	title = db.Column(db.String(20))
	type = db.Column(db.String(20))
	severity = db.Column(db.String(20))
	frequency = db.Column(db.String(20))
	notif2web = db.relationship("notification2websites", backref="notificationheaders", lazy="select")
	notif2prod = db.relationship("notification2products", backref="notificationheaders", lazy="dynamic")
	notif2search = db.relationship("notification2searchstring", backref="notificationheaders", lazy="dynamic")
	notif2contact = db.relationship("notification2contacts", backref="notificationheaders", lazy="dynamic")
	notifrules = db.relationship("notificationrules", backref="notificationheaders", lazy="dynamic")

	#def __repr__(self):
		#return "{'id': '%s', 'notification_uuid': '%s', 'user_uuid': '%s', 'company_uuid': '%s', 'title': '%s', 'type': '%s', 'severity': '%s', 'frequency': '%s'}" % (self.id, self.notification_uuid, self.user_uuid, self.company_uuid, self.title, self.type, self.severity, self.frequency)
		#return str(self.id)

	def getData(self):
		response = {}

		response["id"] = self.id
		response["notification_uuid"] = self.notification_uuid
		response["user_uuid"] = self.user_uuid
		response["company_uuid"] = self.company_uuid
		response["title"] = self.title
		response["type"] = self.type
		response["severity"] = self.severity
		response["frequency"] = self.frequency

		return response

	def getSpecificColumn(self, indexList):
		cols = self.getData()
		response = {}

		for index in indexList:
			response[index] = cols[index]

		return response

#----------------------------------------------------------------

class notificationcontacts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	contact_uuid = db.Column(db.String(20), unique=True)
	email_address = db.Column(db.String(20))
	firstname = db.Column(db.String(20))
	lastname = db.Column(db.String(20))
	notif2contact = db.relationship("notification2contacts", backref="notificationcontacts", lazy="dynamic")

	#def __init__(self, email_address):
		#self.email_address = email_address

	#def __repr__(self):
		#return  (self.email_address)

	def getData(self):
		return {
			"id": self.id,
			"contact_uuid": self.contact_uuid,
			"email_address": self.email_address,
			"firstname": self.firstname,
			"lastname": self.lastname
		}

	def getSpecificColumn(self, indexList):
		cols = self.getData();
		response = {}
		for index in indexList:
			response[index] = cols[index]

		return response

#----------------------------------------------------------------

class notification2websites(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	notification_uuid = db.Column(db.String(20), db.ForeignKey("notificationheaders.notification_uuid"))
	website_uuid = db.Column(db.String(20))

#----------------------------------------------------------------

class notification2products(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	notification_uuid = db.Column(db.String(20), db.ForeignKey("notificationheaders.notification_uuid"))
	product_uuid = db.Column(db.String(20))

#----------------------------------------------------------------

class notification2searchstring(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	notification_uuid = db.Column(db.String(20), db.ForeignKey("notificationheaders.notification_uuid"))
	searchstring_uuid = db.Column(db.String(20))

#----------------------------------------------------------------

class notification2contacts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	notification_uuid = db.Column(db.String(20), db.ForeignKey("notificationheaders.notification_uuid"))
	contact_uuid = db.Column(db.String(20), db.ForeignKey("notificationcontacts.contact_uuid"))

#----------------------------------------------------------------

class notificationruletemplate(db.Model):
	rule_template_id = db.Column(db.Integer(), primary_key=True)
	templates = db.Column(db.String(20))
	notifrules = db.relationship("notificationrules", backref="notificationruletemplate", lazy="dynamic")

#----------------------------------------------------------------

class notificationrules(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rule_template_id = db.Column(db.Integer, db.ForeignKey("notificationruletemplate.rule_template_id"))
	rule_uuid = db.Column(db.String(20))
	notification_uuid = db.Column(db.String(20), db.ForeignKey("notificationheaders.notification_uuid"))
	arg1 = db.Column(db.String(20))

#----------------------------------------------------------------




#sampleContact = notificationcontacts(email_address='temp')
#db.session.add(sampleContact)
#db.session.commit()


#sample1 = (notificationheaders.query\
#	.join(notification2websites)\
#	.add_columns(\
#		notificationheaders.notification_uuid,\
#		notification2websites.website_uuid\
#	).all())


#sample2 = db.session.query(notificationheaders, notification2websites)\
#	.add_columns(\
#		notificationheaders.notification_uuid,\
#		notificationheaders.title,\
#		notificationheaders.type,\
#		notificationheaders.severity,\
#		notificationheaders.frequency,\
#		notification2websites.website_uuid,\
#		notification2products.product_uuid,\
#		notification2searchstring.searchstring_uuid\
#	)\
#	.filter(notificationheaders.notification_uuid == notification2websites.notification_uuid)\
#	.filter(notificationheaders.notification_uuid == notification2products.notification_uuid)\
#	.filter(notificationheaders.notification_uuid == notification2searchstring.notification_uuid)\
#	.filter(notificationheaders.notification_uuid == 'nh-3')\
#	.all()


#for number in sample1:
	#print(number[0].getData())
	#print(number[1].getData())
	#print(number)

#dat = {
#	"retailers":[{"email_address":"testing"}]
#}

#db.session.add(notificationcontacts(email_address = dat["retailers"][0]["email_address"]))
#db.session.commit()

if __name__ == "__main__":
	db.create_all()
	app.run(host="0.0.0.0", port=5432, debug=True)
