import logging

formatter = logging.Formatter(
    "%(asctime)s - %(module)s - %(funcName)s - line:%(lineno)d - %(levelname)s - %(message)s"
)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
# fh = logging.FileHandler(filename='./server.log')
ch.setFormatter(formatter)
# fh.setFormatter(formatter)
logger.addHandler(ch) #Exporting logs to the screen
# logger.addHandler(fh) #Exporting logs to a file