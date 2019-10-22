#!/usr/bin/env python
# coding: utf-8
from flask import Flask, url_for
from flask import request
from flask import jsonify
import server_queries

VERSION = 1
app = Flask(__name__)

@app.route('/')
def api_root():
	return 'Welcome'


@app.route('/database_update', methods=['GET','POST'])
def post_database_update():
	tag_name = "Cluster updated"
	val = server_queries.createinicialjson(request.json,tag_name)
	json_req = server_queries.getUpdates()
	val2 = {"custom_properties":{"error":0,"message":"","result":json_req,"classifier":VERSION}}
	val = {**val,**val2}
	return jsonify(val)


@app.route('/search_address', methods=['GET','POST'])
def search_address():
	tag_name = "Address Classification"
	if request.method == 'GET':
		val = server_queries.createinicialjsonfromget(request.args,tag_name)
		if ('key' in request.args) and ('currency' in request.args):
			adds = request.args['key']
			cash = request.args['currency']
		else:
			val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address or currency not found","result":"","classifier":VERSION}}
			val = {**val,**val2}		
			return jsonify(val)
	else:
		val = server_queries.createinicialjson(request.json,tag_name)
		if ('key' in request.json) and ('tag_optional' in request.json):
			adds = request.json['key']
			tag = request.json['tag_optional']
			cash = tag['currency']
		else:
			val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address or currency not found","result":"","classifier":VERSION}}
			val = {**val,**val2}
			return jsonify(val)

	if ((adds !="") and (len(cash)==3)):        
		val2 = server_queries.getAddressEvaluation(adds,cash)
		val = {**val,**val2}
	elif (len(cash)!=3):
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Currency lenght not correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
	else:
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
		val = {**val,**val2}
	return jsonify(val)      


@app.route('/class_checker', methods=['GET','POST'])
def api_class_checker():
	aconf = 100
	tag_name = "Class Confidence"
	if request.method == 'GET':
		val = server_queries.createinicialjsonfromget(request.args,tag_name)
		if ('key' in request.args) and ('currency' in request.args) and ('class' in request.args) and ('confidence' in request.args):
			adds = request.args['key']
			cash = request.args['currency']
			actor = request.args['class']
			actor = actor.lower()
			aconf = request.args['confidence']	
		else:
			val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address or currency or class or confidence not found","result":"","classifier":VERSION}}
			val = {**val,**val2}
			return jsonify(val)
	else:
		val = server_queries.createinicialjson(request.json,tag_name)
		if ('key' in request.json) and ('tag_optional' in request.json) and ('custom_properties' in request.json):
			adds = request.json['key']
			tag = request.json['tag_optional']
			cash = tag['currency']
			actor = tag['actor_type']
			actor = actor.lower()
			custom = request.json['custom_properties']
			aconf = custom['confidence']
		else:
			val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address or currency or class or confidence not found","result":"","classifier":VERSION}}
			val = {**val,**val2}
			return jsonify(val)

	try: aconf = int(aconf)
	except: 
		val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Confidence value not correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
		return jsonify(val)
	else: 
		classlist = ["exchange","gambling","market","miner","mixer","service"]
		if ((adds !="") and (len(cash) == 3) and (actor in classlist) and (aconf >=0 and aconf<=100)):
			if (actor == 'exchange'): aclass = 'exc'
			elif (actor == 'gambling'): aclass = 'gmb'
			elif (actor == 'market'): aclass = 'mrk'
			elif (actor == 'miner'): aclass = 'mpo'
			elif (actor == 'mixer'): aclass = 'mxr'
			elif (actor == 'service'): aclass = 'ser'
			val2 = server_queries.classificationChecker(adds,cash,aclass,aconf)
			val = {**val,**val2}
		elif (aconf < 0 or aconf > 100):
			val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Confidence value not correct","result":"","classifier":VERSION}}
			val = {**val,**val2}
		elif (actor not in classlist):
			val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Class not exist","result":"","classifier":VERSION}}
			val = {**val,**val2}
		elif (len(cash)!=3):
			val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Currency lenght not correct","result":"","classifier":VERSION}}
			val = {**val,**val2}
		else:
			val2 = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not correct","result":"","classifier":VERSION}}
			val = {**val,**val2}
		return jsonify(val)
	
@app.route('/list_classes', methods=['GET','POST'])
def api_list_classes():
	tag_name = "List Classes"
	if request.method == 'GET':
		val = server_queries.createinicialjsonfromget(request.args,tag_name)
		if ('currency' in request.args):
			cash = request.args['currency']
		else:
			val = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Currency not found","result":"","classifier":VERSION}}
			return jsonify(val)
	else:
		val = server_queries.createinicialjson(request.json,tag_name)
		if ('tag_optional' in request.json):
			tag = request.json['tag_optional']
			cash = tag['currency']
		else:
			val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Currency not found","result":"","classifier":VERSION}}
			val = {**val,**val2}
			return jsonify(val)
	if (len(cash) == 3):
		val2 = server_queries.listClasses(cash)
		val = {**val,**val2}
	else:
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Currency lenght not correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
	return jsonify(val)
    
@app.route('/list_addresses', methods=['GET','POST'])
def api_list_addresses():
	tag_name = "Address List"
	if request.method == 'GET':
		val = server_queries.createinicialjsonfromget(request.args,tag_name)
		if ('key' in request.args) and ('currency' in request.args):
			adds = request.args['key']
			cash = request.args['currency']
		else:
			val = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address or currency not found","result":"","classifier":VERSION}}
			return jsonify(val)
	else:
		val = server_queries.createinicialjson(request.json,tag_name)
		if ('key' in request.json) and ('tag_optional' in request.json):
			adds = request.json['address']     
			tag = request.json['tag_optional']
			cash = tag['currency']
		else:
			val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address or currency not found","result":"","classifier":VERSION}}
			val = {**val,**val2}
			return jsonify(val)
	if ((adds!="") and (len(cash) == 3)):
		val2 = server_queries.first100useraddresses(user,cash)
		val = {**val,**val2}
	elif (len(cash)!=3):
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Currency lenght not correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
	else:
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address ot correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
	return jsonify(val)
    
@app.route('/list_user_addresses', methods=['GET','POST'])
def api_list_user_addresses():
	tag_name = "User Address List"
	if request.method == 'GET':
		val = server_queries.createinicialjsonfromget(request.args,tag_name)
		if ('user' in request.args) and ('currency' in request.args):
			user = request.args['user']
			cash = request.args['currency']
		else:
			val = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"User or currency not found","result":"","classifier":VERSION}}
			return jsonify(val)
	else:
		val = server_queries.createinicialjson(request.json,tag_name)
		if ('tag_optional' in request.json) and ('custom_properties' in request.json):
			tag = request.json['tag_optional']
			cash = tag['currency']
			custom = request.json['custom_properties']
			user = custom['user']
		else:
			val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"User or currency not found","result":""}}
			val = {**val,**val2}
			return jsonify(val)
	if ((user!="") and (len(cash) == 3)):
		val = server_queries.first100useraddresses(user,cash)
	elif (len(cash)!=3):
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Currency lenght not correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
	else:
		val2 = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address ot correct","result":"","classifier":VERSION}}
		val = {**val,**val2}
	return jsonify(val)

@app.route('/search_jsondata', methods=['POST'])
def search_address_from_json():
	tag_name = "Address Classification"
	if request.method == 'POST':
		val = request.json #server_queries.createimportedjson(request.json,tag_name)
		if ('key' in request.json) and ('tag_optional' in request.json) and ('key_type' in request.json):
			key_type = request.json['key_type']
			if key_type == 'a':
				adds = request.json['key']
				tag = request.json['tag_optional']
				cash = tag['currency']
			else:
				val2 = {"custom_properties":{"error":1,"message":"Key type is not valid","result":"","classifier":VERSION}}
				val = server_queries.createReturnedJson(val,val2,tag_name)
				return jsonify(val)
		else:
			val2 = {"custom_properties":{"error":1,"message":"Address or currency not found","result":"","classifier":VERSION}}
			val = server_queries.createReturnedJson(val,val2,tag_name)
			return jsonify(val)
	if ((adds !="") and (len(cash)==3)):         
		val2 = server_queries.getAddressEvaluation(adds,cash)
	elif (len(cash)!=3):
		val2 = {"custom_properties":{"error":1,"message":"Currency lenght not correct","result":"","classifier":VERSION}}
	else:
		val2 = {"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
	val = server_queries.createReturnedJson(val,val2,tag_name)
	return jsonify(val)

if __name__ == '__main__':
	app.run(host="0.0.0.0")
