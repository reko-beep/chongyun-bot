import logging


logging.basicConfig(
    # filename='fulllogs.log',
    encoding='utf-8',
    #format='[%(asctime)s][%(module)s][%(levelname)s] %(message)s',
    #format='[%(levelname)s][%(module)s] %(message)s',
    format='[%(module)-15s]: %(message)s',
 
    datefmt='%d-%m %I:%M',
    filemode='w',
    level=logging.DEBUG)
logging.raiseExceptions = True



