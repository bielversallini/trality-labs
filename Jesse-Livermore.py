SYMBOLS_NTF  = ["MANABUSD","SANDBUSD","CHZBUSD","ENJBUSD","AXSBUSD","CHRBUSD","ALICEBUSD","THETABUSD"]
SYMBOLS_DEFI = ["LUNABUSD","FTMBUSD","SUSHIBUSD","AVAXBUSD","LINKBUSD","AAVEBUSD","YFIBUSD","UNIBUSD"]

############################################################################################################################

LONG    = "LONG"
SHORT   = "SHORT"
NEUTRAL = "NEUTRAL"

############################################################################################################################

def initialize(state):
    state.signals = {}

############################################################################################################################

def compute_signals(state, symbol, data):
    # TODO
    return

############################################################################################################################

def process_orders(state, symbol, data):
    # TODO
    return

############################################################################################################################

def execute(state, dataMap):
    for symbol, data in dataMap.items(): 
        if data is None:
            return       
        compute_signals(state, symbol, data)

        process_orders(state, symbol, data)

################################################# INTERVALS ################################################################

@schedule(interval= "1h", symbol=SYMBOLS_NTF)
def handler_nft(state, dataMap):
    execute(state, dataMap)

@schedule(interval= "1h", symbol=SYMBOLS_DEFI)
def handler_defi(state, dataMap):
    execute(state, dataMap)

############################################################################################################################