import logging
import datetime
import os

def setupSqlAlchemyLogger() -> None:
    sqlalchemy_logger: logging.Logger = logging.getLogger('sqlalchemy')
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.propagate = False

def initializeLogging() -> None:
    log_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logging.basicConfig(filename=f'./logs/{log_filename}.log', format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')
    setupSqlAlchemyLogger()
    
def getLogger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger