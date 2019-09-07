#!/usr/bin/env python

"""optimize the portfolio mix
"""

import datetime
import random
import csv
import sys

import numpy
from tqdm import tqdm

from boglehead.portfolio import Portfolio
from boglehead.fund import load_all_funds, Fund

# # brute force to survey the landscape
# fund_list = ['VBMFX', 'VFINX', 'VISVX', 'VMVIX']
# proportion_lists = (
#     # [0.25, 0.25, 0.25, 0.25],
#     # [0.4, 0.2, 0.2, 0.2],
#     # [0.2, 0.4, 0.2, 0.2],  # current
#     # [0.2, 0.2, 0.4, 0.2],
#     # [0.2, 0.2, 0.2, 0.4],
#     [0.7, 0.1, 0.1, 0.1],
#     [0.1, 0.7, 0.1, 0.1],
#     [0.1, 0.1, 0.7, 0.1],
#     [0.1, 0.1, 0.1, 0.7],
#     [0.4, 0.4, 0.1, 0.1],
#     [0.4, 0.1, 0.4, 0.1],
#     [0.4, 0.1, 0.1, 0.4],
#     [0.1, 0.4, 0.4, 0.1],
#     [0.1, 0.4, 0.1, 0.4],
#     [0.1, 0.1, 0.4, 0.4],
# )

# # run each set of simulations and print out the median, 25/75 and 5/95
# # confidence intervals
# for proportion_list in proportion_lists:
#     portfolio = Portfolio(fund_list, proportion_list)
#
#     vs = portfolio.simulate(100.0)
#     vs.sort()
#     print proportion_list, vs[50], vs[250], vs[500], vs[750], vs[950]

# limit the analysis to only funds that have data for >10 years
all_funds = load_all_funds()
available_funds = []
min_date = datetime.date.today() - datetime.timedelta(days=365*7)
for fund in all_funds:
    d = datetime.datetime.strptime(fund.min_date(), "%Y-%m-%d").date()
    if d < min_date:
        available_funds.append(fund)

# funds = [Fund("VFIAX"), Fund("VBTLX"), Fund("VMVAX"), Fund("VSIAX")]

# sample the efficient frontier
writer = csv.writer(sys.stdout)
writer.writerow(["mean", "stdev", "portfolio"])
for trial in tqdm(range(1000)):

    # select a random sample of funds and allocations
    n_funds = random.randint(1, 5)
    funds = random.sample(available_funds, n_funds)
    proportions = [random.random() for _ in range(len(funds))]
    norm = sum(proportions)
    proportions = [p/norm for p in proportions]

    # simulate the portfolio
    portfolio = Portfolio(funds, proportions)
    results = portfolio.simulate(100.0, n_mc=30, rebalance_frequency=6*5)

    # record the results
    writer.writerow([
        numpy.mean(results),
        numpy.std(results),
        portfolio.to_json_str(),
    ])
