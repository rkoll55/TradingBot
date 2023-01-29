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
        self.asset = ticker

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

    def set_stoploss(self, entryPrice, trend):
        #Set stoploss: takes price and sets stoploss depending on trend
            #IN: entryPrice and trend (long or short)
            #OUT: stop loss
        try:
            if trend == 'long':
                stopLoss = entryPrice - entryPrice * self.StopLossMargin 
                return stopLoss
            elif trend == 'short':
                stopLoss = entryPrice + entryPrice * self.StopLossMargin 
                return stopLoss
            else:
                raise ValueError
        except Exception as e:
            logging.error("trendal value is not long or short %s" %str(trend))
            sys.exit()
        

    def set_takeprofit(self, entryPrice, trend):
        #Set takeprofit: takes price and sets the takeprofit
            #IN: entryPrice and trend (long or short)
            #OUT: take profit 
        try:
            if trend == 'long':
                takeProfit = entryPrice + entryPrice * self.TakeProfitMargin 
                return takeProfit
            elif trend == 'short':
                takeProfit = entryPrice - entryPrice * self.TakeProfitMargin 
                return takeProfit
            else:
                raise ValueError
        except Exception as e:
            logging.error("trendal value is not long or short %s" %str(trend))
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
         
    def check_position(self, asset, notFound=False):
    #Check Position (whether its open or not)
        #IN ticker, wether the asset should be found on not true means it should not
        #OUT Boolean
        attempt = 1
        maxAttempts = 5

        while attempt < maxAttempts:
            try:
                #position = ask alpaca wrapper for position
                currentPrice = position.current_price
                logging.info('Position checked. Current price is: %.2f' % currentPrice)
                return True
            except: 
                if notFound:
                    logging.info('Position not found, this is good')
                    return False

                logging.info('Waiting for position to be found')
                time.sleep(5)
                attempt += 1
        
        logging.info('Position not found')
        return False 

    def get_shares_amount(self,assetPrice):
        #works out number of shares to buy and sell
        #IN: assetProce
        #OUT: number of shares

        #define max to spend
        maxSpendEquity = 1000
        #calculate total equity from Alpaca API
        #calculate the number of shares
        totalShares = int(maxSpendEquity / assetPrice)
        return totalShares

    def get_current_price(self,asset):
        #Get the current price of the open position
        # IN: Ticker
        # OUT: price
        attempt = 1
        maxAttempts = 5

        while attempt < maxAttempts:
            try:
                #position = ask alpaca wrapper for position
                currentPrice = position.current_price
                logging.info('Position checked. Current price is: %.2f' % currentPrice)
                return currentPrice
            except: 
                logging.info('Position cannot be found, cannot check price, waiting')
                time.sleep(5)
                attempt += 1
        
        logging.error('Position not found')
        return False 

    def get_general_trend(self, asset):
    #Get general trend 
        #IN: 30 minute candles data
        #OUTPUT: UP/ DOWN/ False
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
                return False
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

    def get_rsi(self,asset,trend):
    #Get RSI
        #IN: 5 minute candles data, output of the GT analysus
        #OUT: True/ False
        attempt = 1
        maxAttempts = 10

        try:
            while True:
                #calculate the RSI
                #rsi = ti.rsi(data,14)

                if trend == 'long': #and rsi > 50 and rsi <80
                    logging.info('Trend detected for %s: long'%asset)
                    return True

                elif trend == 'short': #and rsi < 50 and rsi > 20
                    logging.info('Trend detected for %s: short'%asset)
                    return True
                elif attempt <= maxAttempts:
                    time.sleep(60)

                else:
                    logging.info('No trend detected')
                    return False
            
        except Exception as e:
            logging.error("Something went wrong with rsi")
            logging.error(e)
            sys.exit()

    def check_stochastic_crossing(self, asset, trend):
        #check whether the stochastic curves have crossed or not 
        #depending on trend 
            #IN: asset, trend
            #OUT: Boolean 
        #Get stochastic values 
        #Ask for 5 minute candles
        stoch_k, stoch_d = ti.stoch(high,low,close,9,6,9)
        try:
            if trend == 'long' and (stoch_k <= stoch_d):
                logging.info("stoch curves crossed")
                return True 
            elif trend == 'short' and (stoch_k >= stoch_d):
                logging.info("stoch curves crossed")
                return True 
            else:
                return False
        except Exception as e:
            logging.error('Something went wrong with check_stochastic_crossing')
            return True

    def get_stochastic(self,asset,trend):
        #Get Stochastic
        #IN: 5 minute candles data, output of the GT analysus
        #OUT: True/ False
        attempt = 1
        maxAttempts = 10

        try:
            while True:
                #calculate the Stoch
                stoch_k, stoch_d = ti.stoch(high,low,close,9,6,9)

                if trend == 'long' and (stoch_k > stoch_d) and (stoch_k < 80) and (stoch_d < 80): 
                    logging.info('%s stochastic = [%.2f,%.2f]'%(asset,stoch_k, stoch_d))
                    return True

                elif trend == 'short' and (stoch_k < stoch_d) and (stoch_k > 20) and (stoch_d > 20): 
                    logging.info('%s stochastic = [%.2f,%.2f]'%(asset,stoch_k, stoch_d))
                    return True
                elif attempt <= maxAttempts:
                    time.sleep(10)

                else:
                    logging.info('No trend detected')
                    return False
            
        except Exception as e:
            logging.error("Something went wrong with stoch analysis")
            logging.error(e)
            sys.exit()

    def enter_position_mode(self, asset, trend):
    #Enter Position Mode: check positions in paralell
        #check conditions in paralell
        #if check take profit -> get out
        #if check stop loss -> get out 
        #if check stoch crossing (pull 5 minute candle data) -> get out

        #entryprice = ask alpaca
        takeProfit = self.set_takeprofit(entryprice, trend)
        stopLoss = self.set_stoploss(entryprice, trend)

        attempt = 1
        maxAttempts = 1260
        try:
            while True:
                currentPrice = self.get_current_price(asset)
                #checking the takeprofit
                if currentPrice >= takeProfit:
                    logging.info('Take profit met at %.2f, getting out at %.2f'%(takeProfit,currentPrice))
                    return True
                #checking the stoploss
                elif currentPrice <= stopLoss:
                    logging.info('Stip loss met at %.2f, getting out at %.2f'%(stopLoss,currentPrice))
                    return True
                #check if stochastic waves crossed around
                elif self.check_stochastic_crossing(asset,trend):
                    logging.info('Stoch curves crossed at %.2f'%currentPrice)
                    return True
                elif attempt <= maxAttempts:
                    logging.info('Waiting inside position')
                    logging.info('Current price %.2f'%currentPrice)
                    time.sleep(20) 
                else:
                    logging.error('Timeout in enter position mode')
                    return True
        except Exception as e:
            logging.error('Something wrong happened in enter_position_mode function')
            logging.error(e)
            return True

    def run(self):
        
        #LOOP until timeout reached (2h)
        #INITIAL CHECK
        while True:
            #POINT A
            #check the position: check if we have open position with asset
            if self.check_position(self.asset, True):
                logging.info('Thre is already and open position with this asset, aborting')
                return False

            #POINT B
            #GENERAL TREND
            #perform general trend analysis: Detect if its going up/down/no trend 
                #if no trend go back to begenning 
            while True:
                trend = self.get_general_trend(self.asset)
                if not trend:
                    logging.info('No general trend found')
                    return False

                
                #Confirm instant trend
                if not self.get_instant_trend(self.asset,trend):
                    logging.info("instant trend not confirmed, going back")
                # IF FAILED GO BACK TO POINT B
                    continue
                #Confirm RSI 
                if not self.get_rsi(self.asset,trend):
                    logging.info("rsi not confirmed, going back")
                # IF FAILED GO BACK TO POINT B
                    continue
                #Confirm stochastic trend
                if not self.get_stochastic(self.asset,trend):
                    logging.info("stochastic not confirmed, going back")
                # IF FAILED GO BACK TO POINT B
                    continue
                logging.info("all filtering passed")
                break
            #Gets the current price
            self.currentPrice = self.get_current_price(self.asset)
            sharesQuantity = self.get_shares_amount(self.currentPrice)

            #SUBMIT ORDER
            # submit order: interact with broker API
                #if False, abort - go back to start

            #check position see if the position exists
            if not self.check_position(self.asset):
                #cancel the pending order
                continue
                #if False, abort - go back to start

            ##enter position mode
            success = self.enter_position_mode(self.asset, trend)
                #Returns true once we have to get out

            #GET OUT
            #submit order
                #if false keepy retrying 

            #rerun code 

            #changing some documentation for testing