import random
import json

from .fund import Fund

EPSILON = 0.001


class Portfolio(object):

    def __init__(self, funds_list, proportion_list):
        self.funds = funds_list
        self.proportions = proportion_list

        if len(self.funds) != len(self.proportions):
            raise IndexError('funds and proportions must be same length')
        if abs(sum(proportion_list) - 1.0) > EPSILON:
            raise ValueError(
                'proportions should add to 1, not %0.6f' % sum(proportion_list)
            )

        for i, fund in enumerate(self.funds):
            if not isinstance(fund, Fund):
                fund = Fund(fund)
                self.funds[i] = fund

    def to_json_str(self):
        """Capture Portfolio as a json string
        """
        data = {}
        for i in range(len(self.funds)):
            data[self.funds[i].symbol] = self.proportions[i]
        return json.dumps(data)

    def initialize_fund_values(self, value):
        """Assign value to specific funds according to the specified
        proportions.
        """
        # Without loss of generality, can effectively own a single unit of each
        # fund.
        #
        # TODO: This will not be true if we separately split out dividends as
        # dividends are generally handed out on a quarterly basis
        for fund, proportion in zip(self.funds, self.proportions):
            fund.units = 1.0
            fund.price = value * proportion / fund.units

    def value(self):
        return sum(fund.value() for fund in self.funds)

    def simulate_date(self, date):
        for fund in self.funds:
            fund.simulate_date(date)
        return self.value()

    def sell(self, sell_value):
        """Sell `value` off from assets in a rebalanced way"""
        self.rebalance()
        current_value = self.value()
        if sell_value > current_value:
            raise ValueError("can't sell that much")
        sell_ratio = sell_value / current_value
        for fund in self.funds:
            fund.units *= 1 - sell_ratio
        if abs(self.value() - (current_value - sell_value)) > EPSILON:
            raise ValueError("#sellfail")
        return self.value()

    def buy(self, buy_value):
        """Buy `value` from assets in a rebalanced way"""
        self.rebalance()
        current_value = self.value()
        if buy_value < 0:
            raise ValueError("can't buy negative, silly")
        buy_ratio = (buy_value + current_value) / current_value
        for fund in self.funds:
            fund.units *= buy_ratio
        if abs(self.value() - (current_value + buy_value)) > EPSILON:
            raise ValueError("#buyfail")
        return self.value()

    def rebalance(self):
        """rebalance the portfolio, without regard for tax consequences"""
        value = self.value()
        for fund, proportion in zip(self.funds, self.proportions):
            delta_value = fund.value() - value * proportion

            # when it is overvalued relative to the portfolio, sell it. when it
            # is undervalued, buy it
            fund.units *= 1.0 - delta_value / fund.value()

        if abs(value - self.value()) > EPSILON:
            raise ValueError("#rebalancefail")

    def simulate(self, starting_value, n_days=260*10, n_mc=1000,
                 rebalance_frequency=260):
        """this is a stupid simulation that picks a random date to determine
        gains across the portfolio, and is effectively continuously rebalanced.

        run the simulation `n_mc` times over `n_days` days (market is typically
        open ~260 days per year) and rebalance every `rebalance_frequency`
        days.
        """

        # get the universe of dates that we can work with for this portfolio.
        # for now only use dates that have data across all funds
        possible_dates = set(self.funds[0].historical_date_reference.keys())
        for fund in self.funds[1:]:
            possible_dates.intersection_update(
                fund.historical_date_reference.keys()
            )
        possible_dates = list(possible_dates)
        possible_dates.sort()
        possible_dates = possible_dates[1:]  # HACK for Fund.gain

        simulated_final_values = []
        for mc in range(n_mc):
            self.initialize_fund_values(starting_value)

            # # simulate gains based on historical correlations, starting from a
            # # random date in the past
            # i = random.randint(0, len(possible_dates) - 1 - n_days)
            # dates = possible_dates[i:i+n_days]
            # assert len(dates) == n_days
            # for day, date in enumerate(dates):
            #     value = self.simulate_date(date)
            #     if rebalance_frequency and (day+1) % rebalance_frequency == 0:
            #         self.rebalance()

            # simulate gains drawn from historical results. This retains
            # correlations across funds but does not account for day-to-day
            # correlations.
            for day in range(n_days):
                date = random.choice(possible_dates)
                value = self.simulate_date(date)
                if rebalance_frequency and (day+1) % rebalance_frequency == 0:
                    self.rebalance()

            simulated_final_values.append(value)

        return simulated_final_values


if __name__ == '__main__':
    portfolio = Portfolio(
        ['VBMFX', 'VFINX', 'VISVX', 'VMVIX'],
        [0.2, 0.4, 0.2, 0.2],
    )

    simulated_final_values = portfolio.simulate(100.0)
    for v in simulated_final_values:
        print(v)
