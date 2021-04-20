#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import os
import requests
import re
from logger import *
from model import MODEL_VERSION, MODEL_VERSION_NOTE

hostname = '127.0.0.1'
port = 5000

try:
    requests.post('http://{}:{}/predict'.format(hostname, port))
    server_running = True
except:
    server_running = False


class Test_API(unittest.TestCase):

    @unittest.skipUnless(server_running, 'Server is not running')
    def test_train(self):
        json_req = {'mode': 'test'}
        response = requests.post('http://{}:{}/train'.format(hostname,
                                 port), json=json_req)
        complete = re.sub("\W+", '', response.text)
        self.assertEqual(complete, 'true')

    @unittest.skipUnless(server_running, 'Server is not running')
    def test_predict(self):
        json_req = {'query': {'country': 'all', 'year': '2019',
                              'month': '4', 'day': '1'}, 'type': 'dict', 'mode': 'test'}
        response = \
            requests.post('http://{}:{}/predict'.format(hostname,
                          port), json=json_req)
        for (key, value) in response.json().items():
            if key == 'y_pred':
                self.assertIsNotNone(value)

    @unittest.skipUnless(server_running, 'Server is not running')
    def test_logs(self):
        logfilename = 'train-test-all.log'
        response = requests.get('http://{}:{}/logs/{}'.format(hostname,
                                port, logfilename))
        downloadfilename = 'dl-train-test-all.log'
        with open(downloadfilename, 'wb') as fh:
            fh.write(response.content)
        self.assertTrue(os.path.exists(downloadfilename))
        if os.path.exists(downloadfilename):
            os.remove(downloadfilename)


if __name__ == '__main__':
    unittest.main()
