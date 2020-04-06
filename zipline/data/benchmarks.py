#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pandas as pd
import requests
import pandas_datareader.data as pd_reader
import numpy as np
from trading_calendars import get_calendar
from datetime import datetime



def get_benchmark_returns(symbol, first_date, last_date):
    cal = get_calendar('NYSE')
    first_date = datetime(1930,1,1)
    last_date = datetime(2030,1,1)
    dates = cal.sessions_in_range(first_date, last_date)
    data = pd.DataFrame(0.0, index=dates, columns=['close'])
    data = data['close']
    return data.sort_index().iloc[1:]
    	
    	
# https://www.itbook5.com/2019/09/11611/
def get_benchmark_returns__(symbol, first_date, last_date):
    """
	Get a Series of benchmark returns from Yahoo associated with `symbol`.
    Default is `SPY`.
    Parameters
    ----------
    symbol : str
        Benchmark symbol for which we're getting the returns.
    The data is provided by Yahoo Finance
    """
    data = pd_reader.DataReader(
        symbol,
        'yahoo',
        first_date,
        last_date
    )
    data = data['Close']
    data[pd.Timestamp('2008-12-15')] = np.nan
    data[pd.Timestamp('2009-08-11')] = np.nan
    data[pd.Timestamp('2012-02-02')] = np.nan
    data = data.fillna(method='ffill')
    return data.sort_index().tz_localize('UTC').pct_change(1).iloc[1:]


def get_benchmark_returns_old(symbol):
    """
    Get a Series of benchmark returns from IEX associated with `symbol`.
    Default is `SPY`.

    Parameters
    ----------
    symbol : str
        Benchmark symbol for which we're getting the returns.

    The data is provided by IEX (https://iextrading.com/), and we can
    get up to 5 years worth of data.
    """
    r = requests.get(
        'https://api.iextrading.com/1.0/stock/{}/chart/5y'.format(symbol)
    )
    data = r.json()

    df = pd.DataFrame(data)

    df.index = pd.DatetimeIndex(df['date'])
    df = df['close']

    return df.sort_index().tz_localize('UTC').pct_change(1).iloc[1:]
