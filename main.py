SYMBOLS_NTF  = ["MANABUSD","SANDBUSD","CHZBUSD","ENJBUSD","AXSBUSD","CHRBUSD","ALICEBUSD","THETABUSD"]
SYMBOLS_DEFI = ["LUNABUSD","FTMBUSD","SUSHIBUSD","AVAXBUSD","LINKBUSD","AAVEBUSD","YFIBUSD","UNIBUSD"]

############################################################################################################################

LONG    = "LONG"
SHORT   = "SHORT"
NEUTRAL = "NEUTRAL"

OVERBOUGHT = "OVERBOUGHT"
OVERSOLD   = "OVERSOLD"

############################################################################################################################

def initialize(state):    
    state.signals = {}
    state.positions = { 'limit': 10, 'count': 0 }

############################################################################################################################

def resolve_macd(state, data):
    indicator = data.macd(12,26,9).last
    buy = indicator[2] >= 0

    if buy:
        signal = LONG
    else:
        signal = SHORT
        
    state.signals[data.symbol]['macd'] = signal

def resolve_stoch(state, data):
    indicator = data.stoch(8,3,3).last
    buy = indicator[0] >= indicator[1]

    if buy and indicator[0] < 80:
        signal = LONG
    elif buy and indicator[0] >= 80:
        signal = OVERBOUGHT
    elif not buy and indicator[0] > 20:
        signal = SHORT
    elif not buy and indicator[0] <= 20:
        signal = OVERSOLD
    else:
        signal = NEUTRAL

    state.signals[data.symbol]['stoch'] = signal

def resolve_ema(state, data):
    fast_ema = data.ema(3).last
    medium_ema = data.ema(8).last
    slow_ema = data.ema(20).last

    signal = NEUTRAL

    if fast_ema > medium_ema and medium_ema > slow_ema and data.close.last > data.open.last:
        signal = LONG
    elif fast_ema < medium_ema and medium_ema < slow_ema and data.close.last < data.open.last:
        signal = SHORT

    state.signals[data.symbol]['ema'] = signal
    
############################################################################################################################

def compute_signals(state, data):
    resolve_macd(state, data)
    resolve_stoch(state, data)
    resolve_ema(state, data)

############################################################################################################################

def is_long(signals):
    return (signals['macd'] == LONG and signals['stoch'] == LONG) and signals['ema'] == LONG

def is_short(signals):
    return (signals['macd'] == SHORT and signals['stoch'] == SHORT) or signals['ema'] == SHORT

def define_strategy(state, data):
    action = NEUTRAL

    signals = state.signals[data.symbol]

    if is_long(signals):
        action = LONG
    elif is_short(signals):
        action = SHORT

    state.signals[data.symbol]['action'] = action

    if action != NEUTRAL:
        log("{} - The signals are: {}".format(data.symbol, state.signals[data.symbol]), 2)

############################################################################################################################

def process_orders(state, data):

    if  not state.signals[data.symbol]['has_position'] and state.signals[data.symbol]['action'] == LONG and state.positions['count'] < state.positions['limit']:
        log("{} - Opening position: {}".format(data.symbol, state.signals[data.symbol]), 3)
        order_market_value(data.symbol, 50.0)
        state.positions['count'] += 1
        
    elif state.signals[data.symbol]['has_position'] and state.signals[data.symbol]['action'] == SHORT:
        log("{} - Closing position: {}.".format(data.symbol, state.signals[data.symbol]), 3)
        close_position(data.symbol)
        state.positions['count'] -= 1

############################################################################################################################

def execute(state, dataMap):
    for symbol, data in dataMap.items(): 
        if data is None:
            return   
             
        if state.signals.get(symbol) == None:
            state.signals[symbol] = {} 

        state.signals[symbol]['has_position'] = has_open_position(symbol, False)

        compute_signals(state, data)

        define_strategy(state, data)

        process_orders(state, data)

################################################# INTERVALS ################################################################

@schedule(interval= "1h", symbol=SYMBOLS_NTF)
def handler_nft(state, dataMap):
    execute(state, dataMap)

@schedule(interval= "1h", symbol=SYMBOLS_DEFI)
def handler_defi(state, dataMap):
    execute(state, dataMap)

############################################################################################################################