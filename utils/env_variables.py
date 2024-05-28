import os
from utils import logs
from logging import Logger

logger: Logger = logs.getLogger()

def readEnvVariable(ENV_VARIABLE_NAME) -> str:
    ENV_VARIABLE: str | None = os.getenv(ENV_VARIABLE_NAME)
    if ENV_VARIABLE is None or ENV_VARIABLE == '':
        message = f'The env variable {ENV_VARIABLE_NAME} is empty. Please define its value in the .env file'
        logger.exception(message)
        raise Exception(message)
    return ENV_VARIABLE