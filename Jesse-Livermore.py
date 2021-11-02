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

############################################################################################################################

def resolve_macd(state, data):
    indicator = data.macd(12, 26, 9).last
    buy = indicator[0] >= indicator[1] 

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

    state.signals[data.symbol]['stoch'] = signal

def resolve_ema(state, data):
    fast_ema = data.ema(3).last
    medium_ema = data.ema(8).last
    slow_ema = data.ema(20).last

    signal = NEUTRAL

    if fast_ema > medium_ema and medium_ema > slow_ema:
        signal = LONG
    elif fast_ema < medium_ema and medium_ema < slow_ema:
        signal = SHORT

    state.signals[data.symbol]['ema'] = signal
    
############################################################################################################################

def compute_signals(state, data):
    resolve_macd(state, data)
    resolve_stoch(state, data)
    resolve_ema(state, data)
    
    log("The signals for {} are {}".format(data.symbol, state.signals[data.symbol]), 2)

############################################################################################################################

def process_orders(state, data):
    # TODO
    return

############################################################################################################################

def execute(state, dataMap):
    for symbol, data in dataMap.items(): 
        if data is None:
            return   
             
        if state.signals.get(symbol) == None:
            state.signals[symbol] = {} 

        compute_signals(state, data)

        process_orders(state, data)

################################################# INTERVALS ################################################################

@schedule(interval= "1h", symbol=SYMBOLS_NTF)
def handler_nft(state, dataMap):
    execute(state, dataMap)

@schedule(interval= "1h", symbol=SYMBOLS_DEFI)
def handler_defi(state, dataMap):
    execute(state, dataMap)

############################################################################################################################