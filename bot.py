#import all libraries
from traderlib import *
from logger import * 
import sys 

#check our trading account and make general API calls 
def check_account():
    try: 
        pass
    except Exception as e:
        logging.error('Count not get info')
        logging.info(str(e))
        sys.exit()
#close current orders
def clean_open_orders():
    logging.info('List of open orders')
    #logging.info(str(open_orders))
    #for order in open_orders:
        #logging.info('Order %s closed' % str(order.id))
    logging.info("closing orders complete")


#call trading botf
    #IN: string 
    #OUT boolean 
def  main():
    #initialise logger 
    initialise_logger()
    check_account()
    clean_open_orders()
    ticker = input("Write the ticker you want to trade with:")
    trader = Trader(ticker)
    complete_trading = trader.run()

    if not complete_trading:
        logging.info("Trading unsuccesful")

if __name__ == '__main__':
    main()