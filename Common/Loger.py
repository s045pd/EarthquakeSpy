import logging
logging.basicConfig(
    format="[%(asctime)s] >>> %(levelname)s  %(name)s: %(message)s", level=logging.INFO)

def GetLoger(Name):
    return logging.getLogger(Name)