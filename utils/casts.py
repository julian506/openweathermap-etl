import os
from utils import logs
from logging import Logger

logger: Logger = logs.getLogger()

def strToInt(strValue: str) -> int:
    try:
        casted = int(strValue)
        return casted
    except:
        message = f'There was an error casting the string {strValue} into integer'
        logger.exception(message)
        raise Exception(message)