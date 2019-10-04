from flask import Flask,render_template,request
import plotly
import plotly.graph_objs as go

#import pandas as pd
import json

import requests

url = 'XX.XX.XX.XX'
headers = {'Content-Type': 'application/json'}

app = Flask(__name__)

@app.route('/')
def server_app():
	return render_template('index.js')


@app.route('/classification', methods=['POST'])
def classification():
	label=request.form['label_opt']
	if(label=="first"):
		r=first()
		r_json= r.json()
		p1 = r_json['custom_properties']
		if (p1['error'] == 0):
		#if(r_json['error']==0):
			pp = p1['result']
			#pp=r_json['result']
			predict=[0]*6
			predict[0]=round(pp['exchange'],4)
			predict[1]=round(pp['gambling'],4)
			predict[2]=round(pp['market'],4)
			predict[3]=round(pp['miner'],4)
			predict[4]=round(pp['mixer'],4)
			predict[5]=round(pp['service'],4)
			bar = create_plot(predict)
			#return render_template('index_result1.html', plot=bar, result=r_json['result'])
			return render_template('index_result1.html', plot=bar, result=p1['result'],address=r_json['key'],version=r_json['version'])
		else:
			#return render_template('index_error.html', result=r_json['message'])
			return render_template('index_error.html', result=p1['message'])

	elif(label=="second"):
		r=second()
		r_json= r.json()
		#if(r_json['error']==0):
		p1 = r_json['custom_properties']
		if (p1['error']==0):
			#return render_template('index_result2.html', result=r_json['result'])
			return render_template('index_result2.html', result=p1['result'])
		else:
			#return render_template('index_error.html', result=r_json['message'])
			return render_template('index_error.html', result=p1['message'])

	elif(label=="third"):
		r=third()
		r_json= r.json()
		p1 = r_json['custom_properties']
		if (p1['error']==0):
		#if(r_json['error']==0):
			#return render_template('index_result3.html', result=r_json['result'])
			return render_template('index_result3.html', result=p1['result']['value'], confidence=p1['confidence'],address=r_json['key'],version=r_json['version'],tag=r_json['tag_optional'])
		else:
			#return render_template('index_error.html', result=r_json['message'])
			return render_template('index_error.html', result=p1['message'])

def first():
	address=request.form['address']
	#data = {'address':str(address),'currency': 'BTC'}
	data = {"uuid": "{}","version": 1,"key_type": "a", "key": str(address),"tag": "","contributor": "","tag_optional": {"currency": "BTC"}}
	response = requests.post(url+'/search_address', json=data)
	return response

def second():
	#data = {'currency': 'BTC'}
	data = {"uuid": "{}","version": 1,"key_type":  "a","key": "","tag": "","contributor": "","tag_optional": {"currency": "BTC"}}
	response = requests.post(url+'/list_classes', json=data)
	return response

def third():
	address=request.form['address']
	classs=request.form['class']
	confidence=request.form['confidence']
	#data = {'address':str(address),'currency': 'BTC','class': str(classs),'confidence': str(confidence)}
	data = {"uuid": "{}","version": 1,"key_type": "a","key": str(address),"tag": "","contributor": "","tag_optional": {"actor_type": str(classs),"currency": "BTC"},"custom_properties":{"confidence": str(confidence)}}
	response = requests.post(url+'/class_checker', json=data)
	return response

def create_plot(predict):
	labels = ['Exchange','Gambling','Marketplace','MiningPool','Mixer','Service']
	x = [float(predict[i]*100) for i in range(0,len(predict))]
	color=['rgb(217,83,79)','rgb(91,192,222)','rgb(92,184,92)','rgb(240, 173, 78)','rgbrgb(2, 117, 216)','rgb(211, 108, 209)']
	b = sum(x)
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

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8810)

