import logging 
import os 
from datetime import datetime

def initialise_logger():
    logs_path = './logs/' #defines the path 
    try:
        os.mkdir(logs_path)
    except OSError:
        print("Already exists")
    else:
        print("made log dir")

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = now + '.log'
    currentLog_path = logs_path + log_name 
    logging.basicConfig(filename=currentLog_path, format = '%(asctime)s - %(levelname)s: %(message)s', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    