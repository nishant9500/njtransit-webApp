import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/result',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    f = [x for x in request.form.values()]
    #final_features = [np.array(int_features)]
    
    #obs = pd.DataFrame([payload], columns=columns).astype(dtypes)
    #proba = pipeline.predict_proba(obs)[0, 1]
    #prediction = model.predict(obs)

    output = 'output'
    user=f[0]
    pas=f[1]
    origin=f[2]
    c=f[3]
    lat,long=c.split(',')
    dest=f[4]
    dest1,dest2=dest.split(',')
    url='http://njttraindata_tst.njtransit.com:8090/njttraindata.asmx/getTrainScheduleJSON19Rec?username='+user+'&password='+pas+'&station='+origin
    res=requests.get(url)
    m=res.text
    m=m.replace('</string>','')
    g="b'<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<string xmlns=\"http://microsoft.com/webservices/\">"
    t="<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<string xmlns=\"http://microsoft.com/webservices/\">"
    m=m.replace(g,'')
    m=m.replace(t,"")
    contents = json.loads(m)
    stops=pd.read_csv('rail_data/stops.txt')
    #print(stops.head(1))
    #print(contents['STATION'])
    det=contents['STATION']
    det2=det['ITEMS']
    det3=det2['ITEM']
    det4=det3[0]
    r=0
    for i in range(len(det3)):
        r2=det3[i]
        if r2['DESTINATION']==dest1:
            r=i
            det4=det3[r]
    url2='http://njttraindata_tst.njtransit.com:8090/njttraindata.asmx/getTrainMapJSON?username='+user+'&password='+pas+'&trainID='+det4['TRAIN_ID']+'&station='+dest2
    res2=requests.get(url2)
    m=res2.text
    m=m.replace('</string>','')
    g="b'<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<string xmlns=\"http://microsoft.com/webservices/\">"
    t="<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<string xmlns=\"http://microsoft.com/webservices/\">"
    m=m.replace(g,'')
    m=m.replace(t,"")
    contents = json.loads(m)
    met1=contents['Trains']
    met2=met1['Train']
    result='Schedule departure time:'+det4['SCHED_DEP_DATE']+'\n'+'Destination:'+det4['DESTINATION']+'\n'+'Track:'+det4['TRACK']+'\n'+'Status'+det4['STATUS']+'\n'+'Last modified:'+det4['LAST_MODIFIED']
    #result2='Direction:'+met2['DIRECTION']+'STOPS:'+met2['STOPS']
    return render_template('index.html', prediction_text=result)


if __name__ == '__main__':
    app.run(debug = True)
