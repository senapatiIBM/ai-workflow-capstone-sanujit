#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
import os
from model import *


class Test_Model(unittest.TestCase):

    def test_model_train(self):
        data_dir = get_data_dir(train=True)
        model_train(data_dir, test=True)
        self.assertTrue(os.path.exists(MODEL_DIR))

    def test_model_load(self):
        (all_data, all_models) = model_load()
        self.assertEqual(
            'all,eire,france,germany,hong_kong,netherlands,norway,portugal,singapore,spain,united_kingdom', ','.join(all_models.keys()))

    def test_model_predict(self):
        (all_data, all_models) = model_load()
        country = 'all'
        year = '2018'
        month = '01'
        day = '05'
        result = model_predict(country, year, month, day)
        y_pred = result['y_pred']
        self.assertIsNotNone(y_pred[0])


if __name__ == '__main__':
    unittest.main()
