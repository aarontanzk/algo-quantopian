"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS


def initialize(context):
    context.spy = sid(8554)
    context.aapl = sid(700)
    context.trends = []
    schedule_function(
        handle_trading,
        date_rules.every_day(),
        time_rules.market_open(hours=1),
        half_days=False
    )


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    context.output = algo.pipeline_output('pipeline')

    # These are the securities that we are interested in trading each day.
    context.security_list = context.output.index


def rebalance(context, data):
    """
    Execute orders according to our schedule_function() timing.
    """
    pass


def record_vars(context, data):
    """
    Plot variables at the end of each day.
    """
    pass


def get_uptrend(context, data):
    spy_hist = data.history(context.spy, 'price', 200, '1d')
    spy_sma = spy_hist.mean()
    if spy_hist[-1] > spy_sma:
        return True
    return False

def handle_trading(context, data):
    open_orders = get_open_orders()
    trend = get_uptrend(context, data)
    context.trends.append(trend)
    hist = data.history(context.aapl, 'price', 50, '1d')
    sma_50 = hist.mean()
    sma_20 = hist[-20:].mean()
    if context.trends[-1] == False and context.trends[-2] == False:
        # it is a downtrend.
        order_target_percent(context.aapl, 0)
    else:
        # it is an uptrend.
        if sma_20 > sma_50 and context.aapl not in open_orders:
            order_target_percent(context.aapl, 1.0)
        elif sma_50 > sma_20 and context.aapl not in open_orders: 
            order_target_percent(context.aapl, -1.0)