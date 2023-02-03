#import all libraries
from traderlib import *
from logger import * 
import sys 
import general_variables
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST
#check our trading account and make general API calls 
def check_account(api):
    try: 
        
        account = api.get_account()
        if account.status != 'ACTIVE':
            logging.error("Could log into account")
            sys.exit()
    except Exception as e:
        logging.error('Count not get info')
        logging.info(str(e))
        sys.exit()

def check_asset_okay(asset,api):
    #IN: TICKER
    #OUT: TRUE if it exists and is tradable / FALSE otherwise
    try: 
        asset = api.get_asset(asset)
        if asset.tradable:
            return True
        else:
            return False 
    except Exception as e:
        logging.error("Error checking asset")
        sys.exit()

#close current orders
def clean_open_orders(api):
    open_orders = api.list_orders(status='open',limit=100,nested=True)
    logging.info('List of open orders')
    logging.info(str(open_orders))
    for order in open_orders:
        logging.info('Order %s closed' % str(order.id))
    try:
        api.cancel_all_orders()
        logging.info("closing orders complete")
    except Exception as e:
        logging.info("ERROR IN CANCELLING ORDERS")
        sys.exit()


#call trading botf
    #IN: string 
    #OUT boolean 
def  main():
    api = tradeapi.REST(general_variables.Alpaca_api_key_id,general_variables.Alpaca_secret_key,general_variables.Alpaca_endpoint,api_version='v2')
 # type: ignore # type: ignore
    #initialise logger 
    initialise_logger()
    check_account(api)
    clean_open_orders(api)
    ticker = input("Write the ticker you want to trade with:")
  
    check_asset_okay(ticker,api)
    trader = Trader(ticker,api)
    complete_trading = trader.run()

    if not complete_trading:
        logging.info("Trading unsuccesful")

if __name__ == '__main__':
    main()