import os
from utils import logs
from logging import Logger

logger: Logger = logs.getLogger()


def strToInt(strValue: str) -> int:
    try:
        casted = int(strValue)
        return casted
    except:
        raise logs.exceptionLog(
            f"There was an error casting the string {strValue} into integer"
        )
