from flask import Flask, jsonify, render_template, request
from flask_api import status

#import sqlalchemy

import time

import models
import ast

app = Flask(__name__)



#-------------------- C R E A T E ------------------------


#query custom columns
def get_queryCustomCol(mainTable, addTables, addCols, filterCol, filterVal):
	for jT in addTables:
		mainTable = mainTable.join(jT)

	for col in addCols:
		mainTable = mainTable.add_column(col)

	return mainTable.filter(filterCol == filterVal).all()


#----------------------------------
def collect_arrData(list, colName):
	temp = []
	for nth in list:
		tempDict = {}
		for ith in range(len(colName)):
			tempDict[colName[ith]] = nth[ith+1]

		temp.append(tempDict)

	return temp;
#----------------------------------

