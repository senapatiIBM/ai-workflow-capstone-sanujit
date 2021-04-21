#!/usr/bin/env python
"""
Monitor model performance
"""

import os
import re
from datetime import date, datetime, timedelta
import numpy as np
from model import *


def model_monitor(country, start_year, start_month, start_day, number_of_days):

    for d in [start_year, start_month, start_day]:
        if re.search("\D", d):
            raise Exception('ERROR (model_monitor) - invalid year, month or day'
                            )

    print('Loading Models')
    (all_data, all_models) = model_load()
    print('... models loaded: ', ','.join(all_models.keys()))
    data = all_data[country]

    start_date = date(int(start_year), int(start_month), int(start_day))
    end_date = start_date + timedelta(days=number_of_days)
    source_start = datetime.strptime(data['dates'][0], '%Y-%m-%d').date()
    source_end = datetime.strptime(data['dates'][-1], '%Y-%m-%d').date()

    if source_start > start_date:
        start_date = source_start
        print('WARNING (model_monitor) - start date is before date range, adjusting start date')

    if source_end < end_date:
        end_date = source_end
        print('WARNING (model_monitor) - end date is after date range, adjusting end date')

    duration = (end_date - start_date).days

    dates = []
    predictions = []
    actuals = []
    for i in range(duration):
        i_date = start_date + timedelta(days=i)
        i_target_date = i_date.strftime("%Y-%m-%d")
        dates.append(i_target_date)

        y_pred = model_predict(country, i_date.strftime(
            '%Y'), i_date.strftime('%m'), i_date.strftime('%d'))['y_pred'][0]
        predictions.append(y_pred)

        date_index = np.where(data['dates'] == i_target_date)
        if (len(date_index) == 0):
            actuals.append(0)
            print('ERROR (model_monitor) - No entry found for ', i_target_date)
        else:
            idx = date_index[0]
            actual_value = data['y'][idx][0]
            actuals.append(actual_value)

    return(dates, predictions, actuals)


if __name__ == "__main__":

    country = 'all'
    year = '2019'
    month = '05'
    day = '01'
    dates, predictions, actuals = model_monitor(
        country, year, month, day, number_of_days=3)
