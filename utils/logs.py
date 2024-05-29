import logging
import datetime


def setupSqlAlchemyLogger() -> None:
    sqlalchemy_logger: logging.Logger = logging.getLogger("sqlalchemy")
    sqlalchemy_logger.setLevel(logging.WARNING)
    sqlalchemy_logger.propagate = False


def initializeLogging() -> None:
    log_filename: str = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logging.basicConfig(
        filename=f"./logs/{log_filename}.log",
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )
    setupSqlAlchemyLogger()


def getLogger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger


def exceptionLog(message: str) -> Exception:
    logger: logging.Logger = getLogger()
    logger.exception(message)
    raise Exception(message)


def infoLog(message: str) -> None:
    logger: logging.Logger = getLogger()
    logger.info(message)
    print(message)
