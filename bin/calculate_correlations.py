
import datetime
import itertools

import numpy as np
import seaborn as sns
import pandas as pd

from boglehead.fund import load_all_funds


# load all funds that started sufficiently long ago to have a meaningful amount
# of data to analyze
all_funds = load_all_funds()
available_funds = []
min_date = datetime.date.today() - datetime.timedelta(days=365*7)
for fund in all_funds:
    d = datetime.datetime.strptime(fund.min_date(), "%Y-%m-%d").date()
    if d < min_date:
        available_funds.append(fund)
n = len(available_funds)

# calculate the pairwise historical correlations across all pairs of funds
symbols = [fund.symbol for fund in available_funds]
rho_ij = np.zeros((n, n))
for i, j in itertools.combinations(range(n), 2):
    fund_i, fund_j = available_funds[i], available_funds[j]
    rho_ij[i,j] = rho_ij[j,i] = fund_i.correlation(fund_j)
df_rho_ij = pd.DataFrame(rho_ij, symbols, symbols)

# visualize the pairwise historical correlations
# https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec
fig = sns.clustermap(
    df_rho_ij,
    method="average",
    vmin=-1, vmax=1, center=0,
    cmap=sns.diverging_palette(20, 220, n=200),
    xticklabels=1, yticklabels=1,
    square=True
)
fig.savefig("tmp/correlations/clustermap.png")
