from flask import Flask,render_template,request
from cassandra.cluster import Cluster
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json

import server_queries


app = Flask(__name__)

#cluster= Cluster(['10.200.5.39'])


def create_plot(predict):
	labels = ['Exchange','Gambling','Market','Pool','Mixer','Service']
	x = [float(predict[i]*100) for i in range(0,len(predict))]
	color=['rgb(217,83,79)','rgb(91,192,222)','rgb(92,184,92)','rgb(240, 173, 78)','rgbrgb(2, 117, 216)','rgb(211, 108, 209)']
	b = sum(x)
	print(x)
	if (b>100):
		m = max(x)
		summ=0
		for i in range(0,len(x)):
			if x[i] != m:
				summ=summ+x[i] 
		for i in range(0,len(x)):
			if x[i] == m:
				x[i]=100.0-summ
	x_n=[]
	labels_n=[]
	color_n=[]
	for i in range(0,len(x)):
		if(x[i]>0.00):
			x_n.append(x[i])
			labels_n.append(labels[i])
			color_n.append(color[i])

	data=[{
	"values": x_n,
    "labels": labels_n,
    "domain": {"column": 0},
    "name": "Classification",
    "hoverinfo":"label+percent",
    'marker': {'colors': color_n},
    "hole": .4,
    "type": "pie"}]
	graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
	return graphJSON

@app.route('/')
def server_app():
	return render_template('index2.html')

@app.route('/search_address', methods=['POST'])
def search_address():
	
	address=request.form['address']
	if (address!=""):
		rows = server_queries.address_info(address)
		if rows == "Not found":
			return render_template('index_result_null.html', result=address)
		else:
			predict=[0]*6
			user_row=rows[0]
			user = user_row.user
			predict[0]=round(user_row.predict_class1,4)
			predict[1]=round(user_row.predict_class2,4)
			predict[2]=round(user_row.predict_class3,4)
			predict[3]=round(user_row.predict_class4,4)
			predict[4]=round(user_row.predict_class5,4)
			predict[5]=round(user_row.predict_class6,4)
			bar = create_plot(predict)
			print (bar)
			return render_template('index_result.html', plot=bar, result_add=address, result_ent=user)
	else:
		return render_template('index_result_null.html', result=address)

#@app.route('/')
#def api_root():
#	return 'Welcome'

#@app.route('/search_address')
#def api_address_info():
#	if 'address' in request.args:
##		return request.args['address']
#		adds = request.args['address']
##		val = queries2.getAddressEvaluation(adds)
#		val = queries3.getAddressEvaluation(adds)
#		return val
#	else:
#		return 'Not address'

@app.route('/class_checker', methods=['POST'])
def class_checker():
	address=request.form['address']
	aclass=request.form['class']
	aconf=request.form['confidence']
	if (address!="" or aclass!="" or aconf!=""):    
		rows = server_queries.classificationChecker(address,aclass,aconf)
		print(rows)
		user=rows[0][0]
		resultado = rows[1]
		print(resultado)        
		if rows == "Not found":
			return render_template('index_result_null.html', result=address)
		else:
			return render_template('index_result_boolean.html', result_add=address, result_ent=user, result_class=aclass, result_conf=aconf, result_bool=resultado)
	else:
		return render_template('index_result_null.html', result=address)
    
#@app.route('/class_checker')
#def api_class_checker():    
#	if 'address' in request.args:
#		adds = request.args['address']
#		aclass = int(request.args['class'])
##		aclass = 1
#		aconf = float(request.args['confidence'])
##		aconf = 0.98 
##		aconf = 1
#		boolean = server_queries.classificationChecker(adds,aclass,aconf)
#		return boolean
##		return (adds+" "+aclass+" "+aclasstype+" "+aconf)
#	else:
#		return 'Not address'

#@app.route('/search_address/<addressid>')
#def api_search_address(addressid):
#	#adds = "'addressid'"
#	#val = queries2.getAddressEvaluation(adds)
#	#return val
#	return 'You asked for ' +addressid

if __name__ == '__main__':
    app.run(host="10.200.5.39",port=5000)

