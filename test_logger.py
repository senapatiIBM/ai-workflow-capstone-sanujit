#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import os
from logger import *
from model import MODEL_VERSION, MODEL_VERSION_NOTE


class Test_Logger(unittest.TestCase):

    def test_update_train_log(self):
        tag = 'united_states'
        test = True
        logfile = os.path.join('logs', 'train-test-{}.log'.format(tag))
        if os.path.exists(logfile):
            os.remove(logfile)

        update_train_log(
            tag,
            str((100, 10)),
            "{'rmse':0.5}",
            '00:00:01',
            MODEL_VERSION,
            MODEL_VERSION_NOTE,
            test=test,
            )
        self.assertTrue(os.path.exists(logfile))

    def test_update_predict_log(self):
        country = 'united_states'
        test = True
        logfile = os.path.join('logs',
                               'predict-test-{}.log'.format(country))
        if os.path.exists(logfile):
            os.remove(logfile)

        update_predict_log(
            country,
            '[0]',
            '[0.6,0.4]',
            '2018-01-05',
            '00:00:01',
            MODEL_VERSION,
            test=test,
            )
        self.assertTrue(os.path.exists(logfile))


if __name__ == '__main__':
    unittest.main()
