#!/usr/bin/python
# -*- coding: utf-8 -*-
# Standard imports

from flask import Flask, jsonify, request
from flask import render_template, send_from_directory
import argparse
import os
import re
import joblib
import socket
import json
import numpy as np
import pandas as pd
from datetime import datetime

# Model imports

from model import get_data_dir, model_train, model_load, model_predict
from model import MODEL_VERSION, MODEL_VERSION_NOTE

# Create an instance of the class for our use

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/index/')
def about():
    return render_template('index.html')


@app.route('/train', methods=['GET', 'POST'])
def train():
    """
    API endpoint to train the model

    'mode' -  can be used to subset data essentially simulating a train, however in the API it used to set the test flag
    """

    # Check if request contains json formatted data

    if not request.json:
        print('ERROR: train API did not receive request data is JSON format')
        return(jsonify(False))

    # Set the test flag based on mode value

    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True

    print('... training model')
    data_dir = get_data_dir(train=True)
    model = model_train(data_dir, test=test)
    print('... training complete')
    return(jsonify(True))


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    API endpoint for predict function
    """

    # Check if request contains json formatted data

    if not request.json:
        print('ERROR: predict API did not receive request data in JSON format')
        return(jsonify([]))

    # Check if request contains query field in json formatted data

    if 'query' not in request.json:
        print("ERROR: predict API received request, but 'query' is missing")
        return(jsonify([]))

    # Check if request contains type field in json formatted data; if not, set to numpy

    if 'type' not in request.json:
        print("WARNING: predict API received request, but 'type' is missing, set to default value of 'numpy'")
        query_type = 'numpy'

    # Set the test flag based on mode value

    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True

    if request.json['type'] == 'dict':
        pass
    else:
        print('ERROR: predict API only supports dict data types')
        return(jsonify([]))

    # Extract query and set predict parameters

    query = request.json['query']
    country = query['country']
    year = query['year']
    month = query['month']
    day = query['day']

    _result = model_predict(
        country,
        year,
        month,
        day,
        all_models=None,
        test=test
    )
    result = {}

    # Get numpy objects and serialize

    for (key, item) in _result.items():
        if isinstance(item, np.ndarray):
            result[key] = item.tolist()
        else:
            result[key] = item

    return(jsonify(result))


@app.route('/logs/<filename>', methods=['GET'])
def logs(filename):
    """
    API endpoint to fetch logs
    """

    if not re.search('.log', filename):
        print('ERROR: logs API - file requested was not a log file: {}'.format(filename))
        return(jsonify([]))

    log_dir = os.path.join('.', 'logs')
    if not os.path.isdir(log_dir):
        print('ERROR: logs API - cannot find log dir')
        return(jsonify([]))

    file_path = os.path.join(log_dir, filename)
    if not os.path.exists(file_path):
        print('ERROR: logs API - file requested could not be found: {}'.format(filename))
        return(jsonify([]))

    return send_from_directory(log_dir, filename, as_attachment=True)


if __name__ == '__main__':

    # Parse arguments and set debug mode

    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--debug', action='store_true',
                    help='debug flask')
    args = vars(ap.parse_args())

    if args['debug']:
        app.run(debug=True, port=5000)
    else:
        app.run(host='0.0.0.0', threaded=True, port=5000)
