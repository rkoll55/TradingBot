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
                time.sleep(5)
                attempt += 1
        
        logging.info('Position not found')
        return False 

    def get_general_trend(self, asset):
    #Get general trend 
        #IN: 30 minute candles data
        #OUTPUT: UP/ DOWN/ NO TREND
        attempt = 1
        maxAttempts = 10
        try:
            while True:

                #ask for 30 minute candles
                #ema9 = ti.ema(data,9)
                #ema26 = ti.ema(data,26)
                #ema50 = ti.ema(data,50)
                
            #Check EMAs relative position if ema50 > ema26 > ema9
                logging.info('Trend detected for %s: long'%asset)
                return 'long'
                #if ema50 < ema26 < ema9
                logging.info('Trend detected for %s: short'%asset)
                return 'short'
                #if attempts <= maxAttemptL
                logging.info('Trend not cl ear for %s: short'%asset)
                time.sleep(60)
                #else 
                logging.info('Trend not detected for %s'%asset)
                return 'no trend'
        except Exception as e:
            logging.error("Something went wrong with get general trend")
            logging.error(e)
            sys.exit()

    def get_instant_trend(self, asset, trend):
    #Get instant trend 
        #IN: 5 minute candles data
        #OUTPUT: UP/ DOWN/ NO TREND

        #ask for 30 minute candles
        #ema9 = ti.ema(data,9)
        #ema26 = ti.ema(data,26)
        #ema50 = ti.ema(data,50)
        #logging.info('%s instant trend EMAs = [%.2f,%.2f,%.2f]'%(asset,ema9,ema26,ema50))
        attempt = 1
        maxAttempts = 10

        try:

            while True:
                if trend == 'long': #and ema9 > ema 26 and ema26 > ema50
                    logging.info('Trend detected for %s: long'%asset)
                    return True

                elif trend == 'short': #and ema9 < ema 26 and ema26 < ema50
                    logging.info('Trend detected for %s: short'%asset)
                    return True
                elif attempt <= maxAttempts:
                    time.sleep(60)

                else:
                    logging.info('No trend detected')
                    return False
            
        except Exception as e:
            logging.error("Something went wrong with get instant trend")
            logging.error(e)
            sys.exit()

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