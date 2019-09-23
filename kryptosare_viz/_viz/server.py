from flask import Flask,render_template,request
from cassandra.cluster import Cluster
import plotly
import plotly.graph_objs as go

import pandas as pd
import numpy as np
import json



app = Flask(__name__)

cluster= Cluster(['10.200.5.39'])


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
	return render_template('index.html')

@app.route('/search_address', methods=['POST'])
def search_address():
	session = cluster.connect('kryptosare')
	address=request.form['address']

	if(address!=""):
		query = "SELECT user FROM address WHERE address=%s"
		future = session.execute_async(query, [address])
		rows = future.result()
		if(not rows):
			return render_template('index_result_null.html', result=address)
		else:
			user = rows[0][0]
			query = "SELECT * FROM enriched_entity WHERE user=%s"
			prediction = session.execute_async(query, [user])
			rows = prediction.result()
			if(not rows):
				return render_template('index_result_null.html', result=address)
			else:
				predict=[0]*6
				user_row=rows[0]
				predict[0]=round(user_row.predict_class1,4)
				predict[1]=round(user_row.predict_class2,4)
				predict[2]=round(user_row.predict_class3,4)
				predict[3]=round(user_row.predict_class4,4)
				predict[4]=round(user_row.predict_class5,4)
				predict[5]=round(user_row.predict_class6,4)
				bar = create_plot(predict)
		return render_template('index_result.html', plot=bar, result_add=address, result_ent=user)
	else:
		return render_template('index_result_null.html', result=address)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8810)

