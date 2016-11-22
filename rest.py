from flask import Flask, jsonify, render_template, request
from flask_api import status

import time

#import json
#from flask_sqlalchemy import SQLAlchemy

import models
import ast

import recycle

app =  Flask(__name__)

#app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:samatosa@localhost/notifix1"
#db = SQLAlchemy(app)

#--------------------------------------------------------------------



@app.route("/api/frontend/v1/notification/contacts", methods=["GET"])
def getContents():
	response = {
		"registered":[],
		"unregistered":[]
	}

	if(request.headers["Content-Type"] == "application/json"):

		result = models.notificationcontacts.query.all()
		for thisResult in result:
			response["unregistered"].append(thisResult.getSpecificColumn(["firstname", "lastname", "email_address"]))

		return (jsonify(response)), status.HTTP_200_OK

	else:
		return "Err: Content-Type", status.HTTP_400_BAD_REQUEST


@app.route("/api/frontend/v1/notification", methods=["GET"])
def getNotifications():
	dataIn = ast.literal_eval(request.data)
	response = {}

	if(request.headers["Content-Type"] == "application/json"):
		#notificationheaders
		notifHead = models.notificationheaders.query\
				.add_columns(\
					models.notificationheaders.notification_uuid,\
					models.notificationheaders.title,\
					models.notificationheaders.type,\
					models.notificationheaders.severity,\
					models.notificationheaders.frequency\
				)\
				.filter(models.notificationheaders.notification_uuid == dataIn["notification_uuid"])\
				.first()
		response = {\
			"notification_uuid": notifHead.notification_uuid,\
			"title": notifHead.title,\
			"type": notifHead.type,\
			"severity": notifHead.severity,\
			"frequency": notifHead.frequency\
		}


		#notification2websites
		response["retailers"] = recycle.collect_arrData(recycle.get_queryCustomCol(models.notification2websites.query,\
				[],\
				[models.notification2websites.website_uuid],\
				models.notification2websites.notification_uuid,\
				dataIn["notification_uuid"]\
			),["website_uuid"])


		#notification2products
		response["products"] = recycle.collect_arrData(recycle.get_queryCustomCol(models.notification2products.query,\
				[],\
				[models.notification2products.product_uuid],\
				models.notification2products.notification_uuid,\
				dataIn["notification_uuid"]\
			),["product_uuid"])


		#notification2searchstring
		response["searchstring"] = recycle.collect_arrData(recycle.get_queryCustomCol(models.notification2searchstring.query,\
				[],\
				[models.notification2searchstring.searchstring_uuid],\
				models.notification2searchstring.notification_uuid,\
				dataIn["notification_uuid"]\
			),["searchstring_uuid"])


		#notification2recipients
		response["recipients"] = recycle.collect_arrData(recycle.get_queryCustomCol(models.notification2contacts.query,\
				[models.notificationcontacts, models.notificationheaders],\
				[models.notification2contacts.contact_uuid, models.notificationcontacts.email_address],\
				models.notification2contacts.notification_uuid,\
				dataIn["notification_uuid"]\
			),["contact_uuid", "email_address"])


		#notification2rules
		response["rules"] = recycle.collect_arrData(recycle.get_queryCustomCol(models.notificationrules.query,\
				[],\
				[models.notificationrules.rule_uuid, models.notificationrules.rule_template_id, models.notificationrules.arg1],\
				models.notificationrules.notification_uuid,\
				dataIn["notification_uuid"]\
			),["rule_uuid", "rule_template_id", "arg1"])



		#------------------------------------------------------
		return (jsonify(response)), status.HTTP_200_OK

	else:
		return "Err: Content-Type", status.HTTP_400_BAD_REQUEST


@app.route("/api/frontend/v1/notification/headers", methods=["GET"])
def getHeaders():
	response = []

	if(request.headers["Content-Type"] == "application/json"):

		result = models.notificationheaders.query.all()
		for thisResult in result:
			response.append(thisResult.getSpecificColumn(["notification_uuid","title","type","severity"]))

		return (jsonify(response)), status.HTTP_200_OK

	else:
		return "Err: Content-Type", status.HTTP_400_BAD_REQUEST


@app.route("/api/frontend/v1/notification", methods=["POST", "PUT"])
def add_or_edit_notifications():
	dataIn = ast.literal_eval(request.data)
	response = {}

	quick_notifUUID = str(round(time.time()))

	if(request.headers["Content-Type"] == "application/json"):

		if(not dataIn["notification_uuid"]):

			#notificationheaders
			models.db.session.add(\
				models.notificationheaders(\
					notification_uuid = str(quick_notifUUID),\
					title = dataIn["title"],\
					type = dataIn["type"],\
					severity = dataIn["severity"],\
					frequency = dataIn["frequency"]
				)
			)


			#notification2websites
			for nth in dataIn["retailers"]:
				models.db.session.add(\
					models.notification2websites(\
						notification_uuid = str(quick_notifUUID),\
						website_uuid = nth["website_uuid"]
					)
				)


			#notification2products
			for nth in dataIn["products"]:
				models.db.session.add(\
					models.notification2products(\
						notification_uuid = str(quick_notifUUID),\
						product_uuid = nth["product_uuid"]
					)
				)


			#notification2searchstring
			for nth in dataIn["searchstring"]:
				models.db.session.add(\
					models.notification2searchstring(\
						notification_uuid = str(quick_notifUUID),\
						searchstring_uuid = nth["searchstring_uuid"]
					)
				)


			#notification2contacts
			for nth in dataIn["recipients"]:
				models.db.session.add(\
					models.notificationcontacts(\
						email_address = nth["email_address"],\
						contact_uuid = nth["contact_uuid"]
					)
				)

				models.db.session.add(\
					models.notification2contacts(\
						notification_uuid = str(quick_notifUUID),\
						contact_uuid = nth["contact_uuid"]
					)
				)


			#notificationrules
			for nth in dataIn["rules"]:
				models.db.session.add(\
					models.notificationruletemplate(\
						rule_template_id = nth["rule_template_id"]
					)
				)

				models.db.session.add(\
					models.notificationrules(\
						notification_uuid = str(quick_notifUUID),\
						rule_uuid = nth["rule_uuid"],\
						arg1 = nth["arg1"],\
						rule_template_id = nth["rule_template_id"]
					)
				)

			models.db.session.commit()
			response["notification_uuid"] = quick_notifUUID

		else:

			#notificationheaders
			notifHU = models.notificationheaders.query.filter(\
					models.notificationheaders.notification_uuid == dataIn["notification_uuid"]\
				).first()

			notifHU.title = dataIn["title"]
			notifHU.type = dataIn["type"]
			notifHU.severity = dataIn["severity"]
			notifHU.frequency = dataIn["frequency"]


			#notification2websites
			models.db.session.query(models.notification2websites).filter(\
				models.notification2websites.notification_uuid == dataIn["notification_uuid"]\
			).delete(synchronize_session=False)


			#-----------------------------
			for nth in dataIn["retailers"]:
				models.db.session.add(\
					models.notification2websites(\
						notification_uuid = dataIn["notification_uuid"],\
						website_uuid = nth["website_uuid"]
					)
				)



			#notification2products
			models.db.session.query(models.notification2products).filter(\
				models.notification2products.notification_uuid == dataIn["notification_uuid"]\
			).delete(synchronize_session=False)


			#-----------------------------
			for nth in dataIn["products"]:
				models.db.session.add(\
					models.notification2products(\
						notification_uuid = dataIn["notification_uuid"],\
						product_uuid = nth["product_uuid"]
					)
				)



			#notification2searchstring
			models.db.session.query(models.notification2searchstring).filter(\
				models.notification2searchstring.notification_uuid == dataIn["notification_uuid"]\
			).delete(synchronize_session=False)


			#-----------------------------
			for nth in dataIn["searchstring"]:
				models.db.session.add(\
					models.notification2searchstring(\
						notification_uuid = dataIn["notification_uuid"],\
						searchstring_uuid = nth["searchstring_uuid"]
					)
				)



			#notification2contacts
			models.db.session.query(models.notification2contacts).filter(\
				models.notification2contacts.notification_uuid == dataIn["notification_uuid"]
			).delete(synchronize_session=False)


			for nth in dataIn["recipients"]:
				models.db.session.query(models.notificationcontacts).filter(\
					models.notificationcontacts.contact_uuid == nth["contact_uuid"]\
				).delete(synchronize_session=False)


			for nth in dataIn["recipients"]:
				models.db.session.add(\
					models.notificationcontacts(\
						email_address = nth["email_address"],\
						contact_uuid = nth["contact_uuid"]
					)
				)

				models.db.session.add(\
					models.notification2contacts(\
						notification_uuid = dataIn["notification_uuid"],\
						contact_uuid = nth["contact_uuid"]
					)
				)



			#notification2rules
			models.db.session.query(models.notificationrules).filter(\
				models.notificationrules.notification_uuid == dataIn["notification_uuid"]
			).delete(synchronize_session=False)


			for nth in dataIn["rules"]:
				models.db.session.query(models.notificationruletemplate).filter(\
					models.notificationruletemplate.rule_template_id == nth["rule_template_id"]\
				).delete(synchronize_session=False)



			#notificationrules
			for nth in dataIn["rules"]:
				models.db.session.add(\
					models.notificationruletemplate(\
						rule_template_id = nth["rule_template_id"]
					)
				)

				models.db.session.add(\
					models.notificationrules(\
						notification_uuid = dataIn["notification_uuid"],\
						rule_uuid = nth["rule_uuid"],\
						arg1 = nth["arg1"],\
						rule_template_id = nth["rule_template_id"]
					)
				)


			models.db.session.commit()
			response["notification_uuid"] = dataIn["notification_uuid"]


		return (jsonify(response)), status.HTTP_200_OK

	else:
		return "Err: Content-Type", status.HTTP_400_BAD_REQUEST


#----------------------------------------------------


@app.route("/api/frontend/v1/rules", methods=["GET"])
def getRules():
	return jsonify("success"), 200



#--------------------------------------------------------------------

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5432, debug=True)
