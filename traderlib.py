#define asset

#LOOP until timeout reached (2h)
#INITIAL CHECK
#check the position: check if we have open position with asset
    #IN asset (string)
    #OUT True (exists)/False (does not)
#check if position is tradable: check of asset is tradable with broker
    #IN asset (string)
    #OUT True (exists)/False (does not)

#GENERAL TREND
#load 30 minute candles: demand API 30 minute candles
    #IN: asset, time range, candle size
    #OUT: 30 min candles

#perform general trend analysis: Detect if its going up/down/no trend 
    #IN: 30 minute candles data
    #OUTPUT: UP/ DOWN/ NO TREND
    #if no trend go back to begenning 

    #LOOP until timeout reached (30 minutes)
    #load 5 minute candles
        #IN: asset, time range, candle size
        #OUT: 5 min candles
    #perfrom instant trend analysis
        #IN: 30 minute candle data, output of general trend analysis 
        #OUT: True (confirmed), / False (Not confirmed)

    #perform RSI analysis
        #IN: 5 minute candles data, output of the GT analysus
        #OUT: True/ False
    #perform stochastic analysis
        #IN: 5 minute candles data, output of the GT analysus
        #OUT: True/ False

#SUBMIT ORDER
# submit order: interact with broker API
    #IN: # number shares to operate with, asset 
    #OUT: True / False
    #if False, abort - go back to start

#check positionL see if the position exists
    #IN: position ID
    #OUT: True / False

#LOOP until timeout reached (large amount of time)
#ENTER POSITION
    #check conditions in paralell
    #if check take profit -> get out
    #if check stop loss -> get out 
    #if check stoch crossing (pull 5 minute candle data) -> get out

#GET OUT
#submit order
    #IN: number of shares to operate with asset
    #OUT: True / False
    #if false keepy retrying 

#rerun code 