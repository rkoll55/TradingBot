from logger import * 
import sys, os , time , pytz
import tulipy as ti
import pandas as pd 
from datetime import datetime 
from math import ceil 

#define asset
class Trader:
    def __init__(self, ticker):
        logging.info('Trader initialized with %s' %ticker)
        self.StopLossMargin = 0.05
        self.TakeProfitMargin = 0.1

    def is_tradable(self, ticker):
        #check if tradable: ask the broker/API if asset is tradable 
            #IN: asset
            #OUT: Boolean 
        try:
            #Get asset from alpaca wrapper
            if not asset.tradable:
                logging.info("Asset %s is not tradable" %ticker)
                return False
            logging.info("Asset %s is not tradable" %ticker)
            return True
        except:
            logging.info("Asset %s is not answering well" %ticker)
            return False 

    def set_stoploss(self, entryPrice, Direction):
        #Set stoploss: takes price and sets stoploss depending on direction
            #IN: entryPrice and Direction (long or short)
            #OUT: stop loss
        try:
            if Direction == 'long':
                stopLoss = entryPrice - entryPrice * self.StopLossMargin 
                return stopLoss
            elif Direction == 'short':
                stopLoss = entryPrice + entryPrice * self.StopLossMargin 
                return stopLoss
            else:
                raise ValueError
        except Exception as e:
            logging.error("Directional value is not long or short %s" %str(Direction))
            sys.exit()
        

    def take_profit(self, entryPrice, Direction):
        #Set takeprofit: takes price and sets the takeprofit
            #IN: entryPrice and Direction (long or short)
            #OUT: take profit 
        try:
            if Direction == 'long':
                takeProfit = entryPrice + entryPrice * self.TakeProfitMargin 
                return takeProfit
            elif Direction == 'short':
                takeProfit = entryPrice - entryPrice * self.TakeProfitMargin 
                return takeProfit
            else:
                raise ValueError
        except Exception as e:
            logging.error("Directional value is not long or short %s" %str(Direction))
            sys.exit()
        

    #load historical data ####

    def get_open_positions(self, assetId):
        #get open positions
            #IN: ticker 
            #OUT: boolean 
        #positions = ask alpaca wrapper for list of open positions 
        for position in positions:
            if position.symbol == assetId:
                return True
            else:
                return False

    #submit order: gets our order throught the API 
        #IN order data, order type
        #OUT Boolean 

    #Cancel order
        #IN order data
        #OUT Boolean
         
    def check_position(self, asset):
    #Check Position (whether its open or not)
        #IN ticker
        #OUT Boolean
        attempt = 0
        maxAttempts = 5

        while attempt < maxAttempts:
            try:
                #position = ask alpaca wrapper for position
                currentPrice = position.current_price
                logging.info('Position checked. Current price is: %.2f' % currentPrice)
                return True
            except: 
                logging.info('Waiting for position to be found')
                time.sleep(5000)
                attempt += 1
        
        logging.info('Position not found')
        return False 

    #Get general trend 
        #IN: 30 minute candles data
        #OUTPUT: UP/ DOWN/ NO TREND

    #Get RSI
        #IN: 5 minute candles data, output of the GT analysus
        #OUT: True/ False

    #Get Stochastic
        #IN: 5 minute candles data, output of the GT analysus
        #OUT: True/ False

    #Enter Position Mode: check positions in paralell
        #check conditions in paralell
        #if check take profit -> get out
        #if check stop loss -> get out 
        #if check stoch crossing (pull 5 minute candle data) -> get out

    def run():
        pass
    #LOOP until timeout reached (2h)
    #INITIAL CHECK
    #check the position: check if we have open position with asset

    #GENERAL TREND
    #load 30 minute candles: demand API 30 minute candles

    #perform general trend analysis: Detect if its going up/down/no trend 
        #if no trend go back to begenning 

        #LOOP until timeout reached (30 minutes)
        #load 5 minute candles
            #IN: asset, time range, candle size
            #OUT: 5 min candles
        #perfrom instant trend analysis
            #IN: 30 minute candle data, output of general trend analysis 
            #OUT: True (confirmed), / False (Not confirmed)

        #perform RSI analysis
            
        #perform stochastic analysis
            

    #SUBMIT ORDER
    # submit order: interact with broker API
        #if False, abort - go back to start

    #check positionL see if the position exists

    #LOOP until timeout reached (large amount of time)
    #ENTER POSITION

    #GET OUT
    #submit order
        #if false keepy retrying 

    #rerun code 