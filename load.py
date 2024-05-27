import urllib.parse
import os
import urllib
from sqlalchemy.orm import sessionmaker
import uuid as uuid_lib
from sqlalchemy import create_engine
from ManizalesWeather import ManizalesWeather

def upload_data(transformed_weather_data):
    AZURE_ODBC_CONNECTION_STRING: str | None = os.getenv("AZURE_ODBC_CONNECTION_STRING")
    if AZURE_ODBC_CONNECTION_STRING == None:
        raise Exception("AZURE_ODBC_CONNECTION_STRING can not be empty")

    params: str = urllib.parse.quote_plus(AZURE_ODBC_CONNECTION_STRING)
    conn_str: str = f"mssql+pyodbc:///?odbc_connect={params}"

    engine = create_engine(conn_str, echo=True)
    print("connection is ok")

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a new weather record
    new_weather_record = ManizalesWeather(
        uuid_value = uuid_lib.uuid4(),
        datetime = transformed_weather_data["datetime"],
        consulted_at = transformed_weather_data["consulted_at"],
        temp = transformed_weather_data["temp"],
        temp_min = transformed_weather_data["temp_min"],
        temp_max = transformed_weather_data["temp_max"],
        feels_like = transformed_weather_data["feels_like"],
    )

    # Add the new weather record to the session
    session.add(new_weather_record)

    # Commit the session to write the record to the database
    session.commit()

    # Query to check if the insert was successful
    weather_records = session.query(ManizalesWeather).all()

    # Print the weather records
    for record in weather_records:
        print(
            f"UUID: {record.uuid}, Datetime: {record.datetime}, Consulted At: {record.consulted_at}, Temp: {record.temp}, Temp Min: {record.temp_min}, Temp Max: {record.temp_max}, Feels Like: {record.feels_like}"
        )

    session.close()
