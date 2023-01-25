#define asset

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
#perform general trend analysis

#LOOP
#load 5 minute candles
#perfrom instant trend analysis
#perform RSI analysis
#perform stochastic analysis

#SUBMIT ORDER
#ENTER POSITION
#submit order 
#check position

#ENTER POSITION MODE (LOOP)
#check take profit
#check stop loss
#check stoch crossing 

#GET OUT
#check order
#check position 

#rerun code 
print("This is my trading bot")