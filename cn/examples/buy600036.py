#!/usr/bin/env python
#
# Copyright 2014 Quantopian, Inc.
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

from zipline.api import order, record, symbol, set_benchmark
from zipline.finance import commission, slippage
import pandas as pd
import pyfolio as pf
import numpy as np
from zipline import run_algorithm
from zipline.utils.calendars import get_calendar


def initialize(context):
    context.asset = symbol('600036.SH')
    # TODO: change to 沪深300
    set_benchmark(symbol('600016.SH'))
    context.set_commission(commission.PerShare(cost=.0003, min_trade_cost=5.0))
    context.set_slippage(slippage.NoSlippage())


def handle_data(context, data):
    order(context.asset, 100)
    record(ZSYH=data.current(context.asset, 'price'))


# Note: this function can be removed if running
# this algorithm on quantopian.com
def analyze(context=None, perf=None):
    pass


if __name__ == '__main__':
    # start date
    start_date = pd.Timestamp('2019-03-05', tz='Asia/Shanghai')
    # end date
    end_date = pd.Timestamp('2019-03-29', tz='Asia/Shanghai')
    cn_calendar = get_calendar('XSHG')

    ext_set = set(['/Users/buffert/Project/git_buffert/quanter/zipline_root/extension.py'])

    perf = run_algorithm(
        start=start_date,
        end=end_date,
        capital_base=1.0e5,
        initialize=initialize,
        handle_data=handle_data,
        analyze=analyze,
        bundle='custom-db-bundle',
        data_frequency='daily',
        trading_calendar=cn_calendar,
        extensions=ext_set
    )
    print(perf)

    # Extract algo returns and benchmark returns
    returns, positions, transactions = pf.utils.extract_rets_pos_txn_from_zipline(perf)

    print(returns)
    print(positions)
    print(transactions)

    benchmark_period_return = perf['benchmark_period_return']
    print(benchmark_period_return)

    # Convert benchmark returns to daily returns
    # daily_returns = (1 + benchmark_period_return) / (1 + benchmark_period_return.shift()) - 1
    daily_benchmark_returns = np.exp(np.log(benchmark_period_return + 1.0).diff()) - 1

    print(returns)

    # Create tear sheet
    pf.create_full_tear_sheet(returns, positions=positions, transactions=transactions)

    print('Done')

