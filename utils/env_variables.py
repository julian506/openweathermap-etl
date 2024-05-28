import os
from utils import logs


def readEnvVariable(ENV_VARIABLE_NAME: str) -> str:
    ENV_VARIABLE: str | None = os.getenv(ENV_VARIABLE_NAME)
    if ENV_VARIABLE is None or ENV_VARIABLE == "":
        raise logs.exceptionLog(
            f"The env variable {ENV_VARIABLE_NAME} is empty. Please define its value in the .env file"
        )
    return ENV_VARIABLE
