from logger import * 
import sys, os , time , pytz
import tulipy as ti
import pandas as pd 
from datetime import datetime 
from math import ceil 
import general_variables
import alpaca_trade_api as tradeapi
import yfinance as yf 


#define asset
class Trader:
    def __init__(self, ticker,api):
        logging.info('Trader initialized with %s' %ticker)
        self.StopLossMargin = 0.05
        self.TakeProfitMargin = 0.1
        self.asset = ticker
        self.api = api

    def is_tradable(self, ticker):
        #check if tradable: ask the broker/API if asset is tradable 
            #IN: asset
            #OUT: Boolean 
        try:
            #Get asset from alpaca wrapper
            if not ticker.tradable:
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
        

    def load_historical_data(self,ticker,interval,period):
        #load historical stock data
            #IN: ticker, interval, api, entries, limit 
            #OUT: Array with stock data
        try:   
            ticker = yf.Ticker(ticker)
            data = ticker.history(period,interval)
            return data 
        except Exception as e:
            logging.error("Something went wrong loading data")
            sys.exit()
            
    def submit_order(self,type,trend,ticker,quantity,currentPrice):
    #submit order: gets our order throught the API 
        #IN order data, order type
        #OUT Boolean 
        if trend == 'long':
            side = 'buy'
            limitPrice =  round(currentPrice + currentPrice*0.03,2)
        elif trend == 'short':
            side = 'sell'
            limitPrice = round(currentPrice - currentPrice*0.03,2)
        else:
            logging.error("Weird trend entered")
            sys.exit()

        try:
            if type == "limit":
                order = self.api.submit_order( 
                    symbol = ticker, 
                    qty = quantity,
                    side =side, 
                    type=type,
                    time_in_force = 'gtc',
                    limit_price=limitPrice
                )
            elif type == 'market':
                order = self.api.submit_order(
                    symbol=ticker,
                    qty=quantity,
                    side=side,
                    type=type,
                    time_in_force='gtc'
                )

            else:
                logging.error("weird order type was entered")
                sys.exit()

            self.client_order_id = order.id
            
            return True
        except Exception as e:
            logging.error("Could not sumbit order cause of error")
            sys.exit()

    def cancel_pending_order(self,ticker):
        attempt = 1
        maxAttempts = 10
        #Cancel order
        #IN order data
        #OUT Boolean
        while attempt <= maxAttempts:
            try:
                self.api.cancel_order(self.client_order_id)
                logging.info("Order cancelled")
                return True 
            except Exception as e:
                logging.info("something i not working while cancelling waiting")
                time.sleep(6)
                attempt += 1
        logging.error("Could not cancel the order")
        self.api.cancel_all_orders()
        return False
         
    def check_position(self, asset, notFound=False):
    #Check Position (whether its open or not)
        #IN ticker, wether the asset should be found on not true means it should not
        #OUT Boolean
        attempt = 1

        while attempt < general_variables.max_attempts_check_position:
            try:
                position = self.api.get_position(asset)
                currentPrice = position.current_price
                logging.info('Position checked. Current price is: %.2f' % float(currentPrice))
                return True
            except Exception as e:
                print(e) 
                if notFound:
                    logging.info('Position not found, this is good')
                    return False

                logging.info('Waiting for position to be found')
                time.sleep(5)
                attempt += 1
        
        logging.info('Position not found')
        return False 

    def get_shares_amount(self,assetPrice):
        maxSpendEquity = 1000
        #works out number of shares to buy and sell
        #IN: assetProce
        #OUT: number of shares
        
        try:
            
            account = self.api.get_account()
            equity = account.equity
            totalShares = int(maxSpendEquity / assetPrice)
            
            if float(equity) - totalShares*assetPrice > 0:
                return totalShares
            else:
                logging.error("You are too poor to afford this")
                sys.exit()

        except Exception as e:
            logging.error("Could not find equity")
            sys.exit()
        #define max to spend
        #calculate total equity from Alpaca API
        #calculate the number of shares
        


    def get_current_price(self,asset):
        #Get the current price of the open position
        # IN: Ticker
        # OUT: price
        attempt = 1
        maxAttempts = 5

        while attempt < maxAttempts:
            try:
                
                position = self.api.get_position(asset)
                currentPrice = float(position.current_price)
                logging.info('Position checked. Current price is: %.2f' % currentPrice)
                return currentPrice
            except: 
                logging.info('Position cannot be found, cannot check price, waiting')
                time.sleep(5)
                attempt += 1
        
        logging.error('Position not found')
        return False 

    def get_avg_entry_price(self, asset):
        #Get the current price of the open position
        # IN: Ticker
        # OUT: price
        attempt = 1
        maxAttempts = 5

        while attempt < maxAttempts:
            try:
                
                position = self.api.get_position(asset)
                currentPrice = float(position.avg_entry_price)
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
                #50 samples * 30 mins (no weekends and 8 hours a day)
                data = self.load_historical_data(asset,interval="30m",period='5d')
                #ask for 30 minute candles
                ema9 = ti.ema(data.Close.values,9)[-1]
                ema26 = ti.ema(data.Close.values,26)[-1]
                ema50 = ti.ema(data.Close.values,50)[-1]
                
                if ema50 > ema26 > ema9:
                    logging.info('Trend detected for %s: long'%asset)
                    return 'long'
                elif ema50 < ema26 < ema9:
                    logging.info('Trend detected for %s: short'%asset)
                    return 'short'
                elif attempt <= maxAttempts:
                    logging.info('Trend not clear for %s: short'%asset)
                    attempt += 1
                    time.sleep(60*5)
                else: 
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
        attempt = 1
        maxAttempts = 10

        try:

            while True:
                data = self.load_historical_data(asset,interval="5m",period='1d')
                ema9 = ti.ema(data.Close.values,9)[-1]
                ema26 = ti.ema(data.Close.values,26)[-1]
                ema50 = ti.ema(data.Close.values,50)[-1]
                logging.info('%s instant trend EMAs = [%.2f,%.2f,%.2f]'%(asset,ema9,ema26,ema50))
                
                if trend == 'long' and ema9 > ema26 and ema26 > ema50:
                    logging.info('Trend detected for %s: long'%asset)
                    return True

                elif trend == 'short' and ema9 < ema26 and ema26 < ema50:
                    logging.info('Trend detected for %s: short'%asset)
                    return True

                elif attempt <= maxAttempts:
                    time.sleep(60)
                    attempt += 1

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
                data = self.load_historical_data(asset,interval="5m",period='1d')
                rsi = ti.rsi(data.Close.values,14)[-1]

                if trend == 'long' and rsi > 50 and rsi <80:
                    logging.info('Trend detected for %s: long'%asset)
                    return True

                elif trend == 'short' and rsi < 50 and rsi > 20:
                    logging.info('Trend detected for %s: short'%asset)
                    return True
                elif attempt <= maxAttempts:
                    time.sleep(60)
                    attempt += 1
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
    
        try:
            data = self.load_historical_data(asset,interval="5m",period='1d')
            stoch_k, stoch_d = ti.stoch(data.High.values,data.Low.values,data.Close.values,9,6,9)
            stoch_k = stoch_k[-1]
            stoch_d = stoch_d[-1]

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
                data = self.load_historical_data(asset,interval="5m",period='1d')
                stoch_k, stoch_d = ti.stoch(data.High.values,data.Low.values,data.Close.values,9,6,9)
                stoch_k = stoch_k[-1]
                stoch_d = stoch_d[-1]

                if trend == 'long' and (stoch_k > stoch_d) and (stoch_k < 80) and (stoch_d < 80): 
                    logging.info('%s stochastic = [%.2f,%.2f]'%(asset,stoch_k, stoch_d))
                    return True

                elif trend == 'short' and (stoch_k < stoch_d) and (stoch_k > 20) and (stoch_d > 20): 
                    logging.info('%s stochastic = [%.2f,%.2f]'%(asset,stoch_k, stoch_d))
                    return True
                elif attempt <= maxAttempts:
                    time.sleep(60*3)
                    attempt += 1
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

        entryprice = self.get_avg_entry_price(asset)
        takeProfit = self.set_takeprofit(entryprice, trend)
        stopLoss = self.set_stoploss(entryprice, trend)

        attempt = 1
        maxAttempts = 360
        try:
            while True:
                currentPrice = self.get_current_price(asset)
                #checking the takeprofit
                if (trend == 'long') and currentPrice >= takeProfit:
                    logging.info('Take profit met at %.2f, getting out at %.2f'%(takeProfit,currentPrice))
                    return True

                elif (trend == 'short') and currentPrice <= takeProfit:
                    logging.info('Take profit met at %.2f, getting out at %.2f'%(takeProfit,currentPrice))
                    return True

                elif (trend == 'long') and currentPrice <= stopLoss:
                    logging.info('Stip loss met at %.2f, getting out at %.2f'%(stopLoss,currentPrice))
                    return False
                #checking the stoploss
                elif (trend == 'short') and currentPrice <= stopLoss:
                    logging.info('Stip loss met at %.2f, getting out at %.2f'%(stopLoss,currentPrice))
                    return False
                #check if stochastic waves crossed around
                elif self.check_stochastic_crossing(asset,trend):
                    logging.info('Stoch curves crossed at %.2f'%currentPrice)
                    return True
                elif attempt <= maxAttempts:
                    logging.info('Waiting inside position')
                    logging.info('Current price %.2f'%currentPrice)
                    time.sleep(20) 
                    attempt += 1
                else:
                    logging.error('Timeout in enter position mode')
                    return False
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

                '''          
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
                #logging.info("all filtering passed")
                '''
                break
            #Gets the current price
        
            currentPrice = self.load_historical_data(self.asset,interval='5m',period='1d').Close.values[-1]
            if currentPrice == None:
                logging.error("the crrent price returned null")
                sys.exit()
            print(currentPrice)
            self.currentPrice = round(float(currentPrice),2)

            # decide the total amount to invest
            sharesQty = self.get_shares_amount(self.currentPrice)

            logging.info('\nDESIRED ENTRY PRICE: %.2f' % self.currentPrice)

            #SUBMIT ORDER
            # submit order: interact with broker API
                #if False, abort - go back to start
            self.submit_order('limit',trend,self.asset,sharesQty,self.currentPrice)
            #check position see if the position exists
            if not self.check_position(self.asset):
                self.cancel_pending_order(self.asset) 
                #if False, abort - go back to start
                continue

            ##enter position mode
            import pdb; pdb.set_trace()
            success = self.enter_position_mode(self.asset, trend)
               
            oppoTrend = "null"
            if trend == "long":
                oppoTrend = "short"
            elif trend == "short":
                oppoTrend = "long"
            else:
               logging.error("trend did not take value of long or short") 
               sys.exit  
            self.submit_order('market',oppoTrend,self.asset,sharesQty,self.currentPrice)
            #GET OUT
            while True:
                #submit order
                #check that position is not there, if false keep retrying 
                if not self.check_position(self.asset,notFound=True):
                    break

                logging.error("Closing position not working trying again")
                time.sleep(10)
            return success
            #rerun code 

            #changing some documentation for testing