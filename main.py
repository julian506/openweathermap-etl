from dotenv import load_dotenv
from scripts import extract, transform, load
import datetime
import schedule
import time
from logging import Logger
from typing import Any
from utils import casts, env_variables, logs


def etlProcess() -> None:
    logger: Logger = logs.getLogger()

    logger.info("--- STARTING NEW EXECUTION ---")
    logger.info("Extracting data...")
    current_weather_data: dict[str, Any] = extract.extractCurrentWeatherData()
    logger.info(f"The extracted data is the next:\n{current_weather_data}")

    logger.info("Transforming data...")
    transformed_weather_data: dict[str, float | datetime.datetime] = (
        transform.transformExtractedData(current_weather_data)
    )
    logger.info(f"The transformed data is the next:\n{transformed_weather_data}")

    logger.info("Uploading data...")
    load.upload_data(transformed_weather_data)
    logger.info("--- EXECUTION FINISHED ---")


if __name__ == "__main__":
    load_dotenv()

    logs.initializeLogging()
    logger: Logger = logs.getLogger()
    logger.info(f"Starting script at {datetime.datetime.now()}")

    PIPELINE_EXECUTION_INTERVAL_IN_MINUTES: str = env_variables.readEnvVariable(
        "PIPELINE_EXECUTION_INTERVAL_IN_MINUTES"
    )

    PIPELINE_EXECUTION_INTERVAL: int = casts.strToInt(
        PIPELINE_EXECUTION_INTERVAL_IN_MINUTES
    )

    logger.info(f"Sending requests every {PIPELINE_EXECUTION_INTERVAL} minutes")

    schedule.every(PIPELINE_EXECUTION_INTERVAL).seconds.do(etlProcess)
    while True:
        schedule.run_pending()
        time.sleep(1)
