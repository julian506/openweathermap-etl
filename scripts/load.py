import urllib.parse
import os
import urllib
from sqlalchemy.orm import Session
import uuid as uuid_lib
from sqlalchemy import create_engine, desc
from classes.TemperatureData import TemperatureData
from utils import env_variables, logs


def isCurrentRecordNew(session, new_weather_record: TemperatureData) -> bool:
    try:
        latest_record_in_db: TemperatureData = (
            session.query(TemperatureData)
            .order_by(desc(TemperatureData.datetime))
            .first()
        )
    except:
        raise logs.exceptionLog(
            "There was an error trying to retrieve the latest register from the database"
        )

    if latest_record_in_db == None:
        return True
    return new_weather_record.datetime > latest_record_in_db.datetime


def createAzureSession(AZURE_ODBC_CONNECTION_STRING: str) -> Session:
    try:
        params: str = urllib.parse.quote_plus(AZURE_ODBC_CONNECTION_STRING)
        conn_str: str = f"mssql+pyodbc:///?odbc_connect={params}"
        engine = create_engine(conn_str, echo=True)

        logs.infoLog(
            "The connection with the Azure SQL Database has been completed successfully"
        )
        return Session(engine)
    except:
        raise logs.exceptionLog("There was an error creating the Azure Session")


def commitDataIntoDatabase(session: Session, new_weather_record: TemperatureData):
    try:
        session.add(new_weather_record)
        session.commit()
        logs.infoLog("The new record has been successfully commited into the database")
    except:
        raise logs.exceptionLog(
            "There was an error commiting the new data into the database"
        )


def upload_data(transformed_weather_data) -> None:
    AZURE_ODBC_CONNECTION_STRING: str = env_variables.readEnvVariable(
        "AZURE_ODBC_CONNECTION_STRING"
    )

    with createAzureSession(AZURE_ODBC_CONNECTION_STRING) as session:
        new_weather_record = TemperatureData(
            uuid_value=uuid_lib.uuid4(),
            datetime=transformed_weather_data["datetime"],
            consulted_at=transformed_weather_data["consulted_at"],
            temp=transformed_weather_data["temp"],
            temp_min=transformed_weather_data["temp_min"],
            temp_max=transformed_weather_data["temp_max"],
            feels_like=transformed_weather_data["feels_like"],
        )

        if not isCurrentRecordNew(session, new_weather_record):
            logs.infoLog(
                "Current data is not newer than the data existing in the DB. Skiping."
            )
            return

        commitDataIntoDatabase(session, new_weather_record)
    return
