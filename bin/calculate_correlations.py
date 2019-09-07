
import datetime
import itertools

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

# calculate the pairwise historical correlations across all pairs of funds
for fund1, fund2 in itertools.combinations(available_funds, 2):
    rho = fund1.correlation(fund2)
    print(fund1.symbol, fund2.symbol, fund1.min_date(), fund2.min_date(), rho)

# visualize the pairwise historical correlations
# https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec
