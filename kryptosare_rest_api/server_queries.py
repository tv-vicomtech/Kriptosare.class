from cassandra.cluster import Cluster
import uuid

cluster= Cluster(['10.200.10.6'],port=9042)
session = cluster.connect()

def getAddressEvaluation(adds,cash):
	cash = cash.upper()
	if (cash == 'BTC'):
		session.execute('USE kryptosare')
		query = "SELECT user FROM cluster WHERE address=%s"
		future = session.execute_async(query, [adds])
		rows = future.result()
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":""}}
			return result;
		for row in rows:
			usern = row.user
			query = "SELECT * FROM enriched_entity WHERE user=%s"
			prediction = session.execute_async(query, [usern])
			rows2 = prediction.result()
			if(not rows2):
				result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":""}}
				return result;
			row2 = rows2[0]
			resultval = {"user":usern,"exchange":row2.predict_class1,"gambling":row2.predict_class2,"market":row2.predict_class3,"miner":row2.predict_class4,"mixer":row2.predict_class5,"service":row2.predict_class6}
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"","result":resultval}}
		return result
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":""}}
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
			result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":""}}
			return result
		for row in rows:
			confval = {"value":"False"}
			usern = "'"+row.user+"'"
			usern = row.user
			query = "SELECT * FROM enriched_entity WHERE user=%s"
			prediction = session.execute_async(query, [usern])
			rows2 = prediction.result()
			if(not rows2):
				result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":""}}
				return result
			for row2 in rows2:
				if aclass=='exc': conf = row2.predict_class1;
				elif aclass=='gmb': conf = row2.predict_class2;
				elif aclass=='mrk': conf = row2.predict_class3;
				elif aclass=='mpo': conf = row2.predict_class4;
				elif aclass=='mxr': conf = row2.predict_class5;
				elif aclass=='ser': conf = row2.predict_class6;
				else:
					result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":""}}
					return result;
				if (float(conf)*100)>=float(aconf):
					confval = {"value":"True"}
		result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":0,"message":"","result":confval}}
		return result
	else:
		result = {"tag_optional":{"actor_type":actor,"currency":cash},"custom_properties":{"confidence":aconf,"error":1,"message":"Address not found","result":""}}
		return result

def listClasses(cash):
	cash = cash.upper()
	if (cash == 'BTC'):
		session.execute('USE kryptosare')
		rows = session.execute('SELECT * FROM classes')
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Classes not found","result":""}}
			return result;
		resultval = [] 
		for row in rows:
			if row.name == "miningpool": name = "miner"
			elif row.name == "marketplace": name = "market"
			else: name = row.name 
			res = {"currency":cash,"label":row.label,"name":name,"abbreviation":row.abbr}
			resultval.append(res)
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"","result":resultval}}
		return result
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Classes not found","result":""}}
		return result

def first100addresses(adds,cash):
	cash = cash.upper()
	if (cash=="BTC"):
		session.execute('USE kryptosare')
		query = "SELECT user FROM address WHERE address=%s"
		future = session.execute_async(query, [adds])
		rows = future.result()
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":""}}
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
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0, "message":"","result":resultval}}
		return result            
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"Address not found","result":""}}
		return result

def first100useraddresses(user,cash):
	cash = cash.upper()
	if (cash=="BTC"):
		session.execute('USE kryptosare')
		query = "SELECT address FROM address WHERE user=%s limit 100 ALLOW filtering"
		prediction = session.execute_async(query, [user])
		rows = prediction.result()
		if(not rows):
			result = {"tag_optional":{"currency":cash},"custom_properties":{"error":1,"message":"User not found","result":""}}
			return result;
		resultval = [] 
		for row in rows:
				res = {"address":row.address,"user":user,"currency":cash}          
				resultval.append(res)
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"","result":resultval}}
		return result            
	else:
		result = {"tag_optional":{"currency":cash},"custom_properties":{"error":0,"message":"User not found","result":""}}
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
	version = 1
	key_type = 'a'
	key = request['key']
	tag = tag_name
	contributor = "Vicomtech"
	result = {"uuid":"{"+str(uid)+"}","version":version,"key_type":key_type,"key":key,"tag":tag,"contributor":contributor}
	return result

def createinicialjsonfromget(request,tag_name):
	uid = uuid.uuid4()
	version = 1
	key_type = 'a'
	if ('key' in request):
		key = request['key']
	else:
		key = ""
	tag = tag_name
	contributor = "Vicomtech"
	result = {"uuid":"{"+str(uid)+"}","version":version,"key_type":key_type,"key":key,"tag":tag,"contributor":contributor}
	return result
