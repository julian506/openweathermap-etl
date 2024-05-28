import urllib.parse
import os
import urllib
from sqlalchemy.orm import Session
import uuid as uuid_lib
from sqlalchemy import create_engine, desc
from classes.ManizalesWeather import ManizalesWeather
from utils import env_variables, logs
from logging import Logger

logger: Logger = logs.getLogger()


def isCurrentRecordNew(session, new_weather_record: ManizalesWeather) -> bool:
    try:
        latest_record_in_db: ManizalesWeather = (
            session.query(ManizalesWeather)
            .order_by(desc(ManizalesWeather.datetime))
            .first()
        )
    except:
        message = "There was an error trying to retrieve the latest register from the database"
        logger.exception(message)
        raise Exception(message)

    if latest_record_in_db == None:
        return True
    return new_weather_record.datetime > latest_record_in_db.datetime


def createAzureSession(AZURE_ODBC_CONNECTION_STRING: str) -> Session:
    try:
        params: str = urllib.parse.quote_plus(AZURE_ODBC_CONNECTION_STRING)
        conn_str: str = f"mssql+pyodbc:///?odbc_connect={params}"
        engine = create_engine(conn_str, echo=True)

        logger.info(
            "The connection with the Azure SQL Database has been completed successfully"
        )
        return Session(engine)
    except:
        message = "There was an error creating the Azure Session"
        logger.exception(message)
        raise Exception(message)


def commitDataIntoDatabase(session: Session, new_weather_record: ManizalesWeather):
    try:
        session.add(new_weather_record)
        session.commit()
        message = "The new record has been successfully commited into the database"
        logger.info(message)
    except:
        message = "There was an error commiting the new data into the database."
        logger.exception(message)
        raise Exception(message)


def upload_data(transformed_weather_data):
    AZURE_ODBC_CONNECTION_STRING: str = env_variables.readEnvVariable(
        "AZURE_ODBC_CONNECTION_STRING"
    )

    with createAzureSession(AZURE_ODBC_CONNECTION_STRING) as session:
        new_weather_record = ManizalesWeather(
            uuid_value=uuid_lib.uuid4(),
            datetime=transformed_weather_data["datetime"],
            consulted_at=transformed_weather_data["consulted_at"],
            temp=transformed_weather_data["temp"],
            temp_min=transformed_weather_data["temp_min"],
            temp_max=transformed_weather_data["temp_max"],
            feels_like=transformed_weather_data["feels_like"],
        )

        if not isCurrentRecordNew(session, new_weather_record):
            message = (
                "Current data is not newer than the data existing in the DB. Skiping."
            )
            logger.info(message)
            print(message)
            return

        commitDataIntoDatabase(session, new_weather_record)
