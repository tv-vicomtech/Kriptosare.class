from cassandra.cluster import Cluster
import uuid

VERSION = 1
cluster= Cluster([''],port=9042)
session = cluster.connect()

def getAddressEvaluation(adds,cash):
	cash = cash.upper()
	if (cash == 'BTC'):
		session.execute('USE kryptosare')
		query = "SELECT user FROM cluster WHERE address=%s"
		future = session.execute_async(query, [adds])
		rows = future.result()
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
			return result;
		for row in rows:
			usern = row.user
			query = "SELECT * FROM enriched_entity WHERE user=%s"
			prediction = session.execute_async(query, [usern])
			rows2 = prediction.result()
			if(not rows2):
				result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
				return result;
			row2 = rows2[0]
			resultval = {"user":usern,"exchange":row2.predict_class1,"gambling":row2.predict_class2,"market":row2.predict_class3,"miner":row2.predict_class4,"mixer":row2.predict_class5,"service":row2.predict_class6}
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"","result":resultval,"classifier":VERSION}}
		return result
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
		return result

def classificationChecker(adds,cash,aclass,aconf):
	cash = cash.upper()
	if (cash=="BTC"):
		if aclass=='exc': actor="Exchange";
		elif aclass=='gmb': actor="Gambling";
		elif aclass=='mrk': actor="Market";
		elif aclass=='mpo': actor="Miner";
		elif aclass=='mxr': actor="Mixer";
		elif aclass=='ser': actor="Service";
		else: actor="";
		session.execute('USE kryptosare')
		query = "SELECT user FROM cluster WHERE address=%s"
		future = session.execute_async(query, [adds])
		rows = future.result()
		if(not rows):
			result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":"","classifier":VERSION}}
			return result
		for row in rows:
			confval = {"value":"False"}
			usern = "'"+row.user+"'"
			usern = row.user
			query = "SELECT * FROM enriched_entity WHERE user=%s"
			prediction = session.execute_async(query, [usern])
			rows2 = prediction.result()
			if(not rows2):
				result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":"","classifier":VERSION}}
				return result
			for row2 in rows2:
				if aclass=='exc': conf = row2.predict_class1;
				elif aclass=='gmb': conf = row2.predict_class2;
				elif aclass=='mrk': conf = row2.predict_class3;
				elif aclass=='mpo': conf = row2.predict_class4;
				elif aclass=='mxr': conf = row2.predict_class5;
				elif aclass=='ser': conf = row2.predict_class6;
				else:
					result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":"","classifier":VERSION}}
					return result;
				if (float(conf)*100)>=float(aconf):
					confval = {"value":"True"}
		result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":0,"message":"","result":confval,"classifier":VERSION}}
		return result
	else:
		result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":"","classifier":VERSION}}
		return result

def listClasses(cash):
	cash = cash.upper()
	if (cash == 'BTC'):
		session.execute('USE kryptosare')
		rows = session.execute('SELECT * FROM classes')
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Classes not found","result":"","classifier":VERSION}}
			return result;
		resultval = [] 
		for row in rows:
			if row.name == "miningpool": name = "miner"
			elif row.name == "marketplace": name = "market"
			else: name = row.name 
			res = {"currency":cash,"label":row.label,"name":name,"abbreviation":row.abbr}
			resultval.append(res)
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"","result":resultval,"classifier":VERSION}}
		return result
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Classes not found","result":"","classifier":VERSION}}
		return result

def first100addresses(adds,cash):
	cash = cash.upper()
	if (cash=="BTC"):
		session.execute('USE kryptosare')
		query = "SELECT user FROM address WHERE address=%s"
		future = session.execute_async(query, [adds])
		rows = future.result()
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
			return result;
		resultval = []
		for row in rows:
			confval = "False"
			usern = row.user
			query = "SELECT address FROM address WHERE user=%s limit 100 ALLOW filtering"
			prediction = session.execute_async(query, [usern])
			rows2 = prediction.result() 
			for row2 in rows2:
				res = {"address":row2.address,"user":usern,"currency":cash}          
				resultval.append(res)
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0, "message":"","result":resultval,"classifier":VERSION}}
		return result            
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
		return result

def first100useraddresses(user,cash):
	cash = cash.upper()
	if (cash=="BTC"):
		session.execute('USE kryptosare')
		query = "SELECT address FROM address WHERE user=%s limit 100 ALLOW filtering"
		prediction = session.execute_async(query, [user])
		rows = prediction.result()
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"User not found","result":"","classifier":VERSION}}
			return result;
		resultval = [] 
		for row in rows:
				res = {"address":row.address,"user":user,"currency":cash}          
				resultval.append(res)
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"","result":resultval,"classifier":VERSION}}
		return result            
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"User not found","result":"","classifier":VERSION}}
		return result

def getUpdates():
	session.execute('USE kryptosare')
	query = "SELECT * FROM cluster_update LIMIT 1"
	future = session.execute_async(query, [])
	rows = future.result()
	if(not rows):
		result = {"timestamp":"100000000","block":"0"}
	else:
		result = {"timestamp":rows[0].timestamp,"block":rows[0].block}
	return result


def createinicialjson(request,tag_name):
	uid = uuid.uuid4()
	#version = 1
	key_type = 'a'
	key = request['key']
	tag = tag_name
	contributor = "Vicomtech"
	result = {"uuid":"{"+str(uid)+"}","version":VERSION,"key_type":key_type,"key":key,"tag":tag,"contributor":contributor}
	return result

def createinicialjsonfromget(request,tag_name):
	uid = uuid.uuid4()
	#version = 1
	key_type = 'a'
	if ('key' in request):
		key = request['key']
	else:
		key = ""
	tag = tag_name
	contributor = "Vicomtech"
	result = {"uuid":"{"+str(uid)+"}","version":VERSION,"key_type":key_type,"key":key,"tag":tag,"contributor":contributor}
	return result

def getAddressFromJsonEvaluation(adds,cash):
	cash = cash.upper()
	if (cash == 'BTC'):
		session.execute('USE kryptosare')
		query = "SELECT user FROM address WHERE address=%s"
		future = session.execute_async(query, [adds])
		rows = future.result()
		if(not rows):
			result = {"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
			return result;
		for row in rows:
			usern = row.user
			query = "SELECT * FROM enriched_entity WHERE user=%s"
			prediction = session.execute_async(query, [usern])
			rows2 = prediction.result()
			if(not rows2):
				result = {"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
				return result;
			row2 = rows2[0]
			resultval = {"user":usern,"exchange":row2.predict_class1,"gambling":row2.predict_class2,"market":row2.predict_class3,"miner":row2.predict_class4,"mixer":row2.predict_class5,"service":row2.predict_class6}
		result = {"custom_properties":{"error":0,"message":"","result":resultval,"classifier":VERSION}}
		return result
	else:
		result = {"custom_properties":{"error":1,"message":"Address not found","result":"","classifier":VERSION}}
		return result

def createReturnedJson(val,val2,tag_name):
	uid = val['uuid']
	version = val['version']
	key_type = val['key_type']
	key = val['key']
	tag = val['tag']+', '+tag_name
	contributor = val['contributor']+', Vicomtech'
	result = {"uuid":uid,"version":version,"key_type":key_type,"key":key,"tag":tag,"contributor":contributor}
	if ('tag_optional' in val):
		tag_op = val['tag_optional']
		result2 = {"tag_optional":tag_op}
		result = {**result,**result2}
	if ('contributor_optional' in val):
		cont_op = val['contributor_optional']
		result2 = {"contributor_optional":cont_op}
		result = {**result,**result2}
	result = {**result,**val2}
	return result