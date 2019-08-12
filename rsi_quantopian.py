"""
This is a template algorithm on Quantopian for you to adapt and fill in.
"""
import quantopian.algorithm as algo
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.filters import QTradableStocksUS
import talib

PERIOD, UB, LB = 14, 70, 30
def initialize(context):
    """
    Called once at the start of the algorithm.
    """
    # AAPL, MSFT, and SPY
    context.assets = [sid(24), sid(5061), sid(8554)]
    context.sym = symbol('AAPL')
    context.i = 0

    # Rebalance every day, 1 hour after market open.
    algo.schedule_function(
        rebalance,
        algo.date_rules.every_day(),
        algo.time_rules.market_open(hours=1),
    )

    # Record tracking variables at the end of each day.
    algo.schedule_function(
        record_vars,
        algo.date_rules.every_day(),
        algo.time_rules.market_close(),
    )

    # Create our dynamic stock selector.
    algo.attach_pipeline(make_pipeline(), 'pipeline')


def make_pipeline():
    """
    A function to create our dynamic stock selector (pipeline). Documentation
    on pipeline can be found here:
    https://www.quantopian.com/help#pipeline-title
    """

    # Base universe set to the QTradableStocksUS
    base_universe = QTradableStocksUS()

    # Factor of yesterday's close price.
    yesterday_close = USEquityPricing.close.latest

    pipe = Pipeline(
        columns={
            'close': yesterday_close,
        },
        screen=base_universe
    )
    return pipe


def before_trading_start(context, data):
    """
    Called every day before market open.
    """
    
    portfolio_cash = context.portfolio.cash
    print("portfolio cash: ")
    print(portfolio_cash)
    portfolio_positions = context.portfolio.positions
    print("portfolio positions: ")
    print(portfolio_positions)
   
    portfolio_open_orders = get_open_orders(24)
    print("portfolio open orders")
    print(portfolio_open_orders)
    
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


def handle_data(context, data):
    
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return
    
    # Compute averages
    # history() has to be called with the same params
    # from above and returns a pandas dataframe.
    short_mavg = data.history(context.sym, 'price', 1, '1d').mean()
    long_mavg = data.history(context.sym, 'price', 5, '1d').mean()
    
    # Trading logic
    #print(str(short_mavg) + " " + str(long_mavg))
 
    prices = data.history(context.sym, 'price', PERIOD + 1, '1d')  
    rsi = talib.RSI(prices, PERIOD)[-1]  
    if data.can_trade(context.sym):  
       if rsi >= UB and rsi >= LB: 
          print("SELL")
          #order_target_percent(context.sym, 1)  
       elif rsi <= LB and rsi <= UB:
          print("BUY")
          #order_target_percent(context.sym, 0)  
       else:
          print("NOTHING")
    """
    if short_mavg < long_mavg:
        order(context.sym, -100)
        print("SELL")
       #portfolio_positions = context.portfolio.positions
        #print(portfolio_positions)
        
    if short_mavg > long_mavg:
        # order_target orders as many shares as needed to
        # achieve the desired number of shares.
        order(context.sym, 100)
        #print("BUY 100")
        portfolio_positions = context.portfolio.positions
        #print(portfolio_positions)
    """   
    # Save values for later inspection
    record(
           
           rsi = rsi, UB = UB, LB = LB,
           )