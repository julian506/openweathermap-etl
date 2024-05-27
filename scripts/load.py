import urllib.parse
import os
import urllib
from sqlalchemy.orm import sessionmaker
import uuid as uuid_lib
from sqlalchemy import create_engine, desc
from classes.ManizalesWeather import ManizalesWeather
import datetime as datetime_lib


def isCurrentRecordNew(session, new_weather_record: ManizalesWeather) -> bool:
    latest_record_in_db: ManizalesWeather = (
        session.query(ManizalesWeather)
        .order_by(desc(ManizalesWeather.datetime))
        .first()
    )
    if latest_record_in_db == None:
        return True
    return new_weather_record.datetime > latest_record_in_db.datetime


def upload_data(transformed_weather_data):
    AZURE_ODBC_CONNECTION_STRING: str | None = os.getenv("AZURE_ODBC_CONNECTION_STRING")
    if AZURE_ODBC_CONNECTION_STRING == None:
        raise Exception("AZURE_ODBC_CONNECTION_STRING can not be empty")

    params: str = urllib.parse.quote_plus(AZURE_ODBC_CONNECTION_STRING)
    conn_str: str = f"mssql+pyodbc:///?odbc_connect={params}"

    engine = create_engine(conn_str, echo=True)
    print("connection is ok")

    Session = sessionmaker(bind=engine)
    session = Session()

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
        print("Current data is not newer than the data existing in the DB. Skiping.")
        return

    session.add(new_weather_record)

    session.commit()

    session.close()
