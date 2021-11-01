from flask import Flask, request, redirect, url_for, flash, jsonify
import numpy as np
import pickle as p
import json
from keras.models import load_model



app = Flask(__name__)


@app.route('/sports/', methods=['GET'])
def getpred():

    home_team = request.args.get('ht', type = str)
    away_team = request.args.get('at', type = str)
    index_to_test = home_away[(home_away['HomeTeam']==home_team)&(home_away['team']==away_team)].index
    newtest = inputs_data[inputs_data.index == index_to_test[0]]
    results = model.predict(newtest)
    max_val = -1
    index_max = -1

    for i in range(0,3):
        if results[0][i] > max_val:
            max_val = results[0][i]
            index_max = i

    #0 = away win
    mapper = {0:'Away Win', 1:'Draw', 2:'Home Win'}
    response =  jsonify({'result' :mapper[index_max]})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
    # modelfile = 'models/final_prediction.pickle'
    # model = p.load(open(modelfile, 'rb'))
    model = load_model('finalized_model.h5')
    home_away = p.load(open('index_labels.sav', 'rb'))
    inputs_data = p.load(open('testing_set.sav', 'rb'))
    app.run(debug=True, host='0.0.0.0')