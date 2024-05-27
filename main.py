from dotenv import load_dotenv
from scripts import extract, transform, load
import datetime
import schedule
import time
import os

def etlProcess():
    current_weather_data = extract.extractCurrentWeatherData()
    print(current_weather_data)
    transformed_weather_data: dict[str, float | datetime.datetime] = (
        transform.transformExtractedData(current_weather_data)
    )
    print(f"The transformed data: \n {transformed_weather_data}")

    load.upload_data(transformed_weather_data)


if __name__ == "__main__":
    load_dotenv()
    PIPELINE_EXECUTION_INTERVAL_IN_MINUTES: str | None = os.getenv('PIPELINE_EXECUTION_INTERVAL_IN_MINUTES')
    if PIPELINE_EXECUTION_INTERVAL_IN_MINUTES == None:
        raise Exception('PIPELINE_EXECUTION_INTERVAL_IN_MINUTES can not be empty')
    
    try:
        PIPELINE_EXECUTION_INTERVAL = int(PIPELINE_EXECUTION_INTERVAL_IN_MINUTES)
    except:
        raise Exception("There was an error processing the PIPELINE_EXECUTION_INTERVAL_IN_MINUTES env variable. Please only send numbers.")
        
    print(f"Sending requests every {PIPELINE_EXECUTION_INTERVAL} minutes")
    
    schedule.every(PIPELINE_EXECUTION_INTERVAL).minutes.do(etlProcess)
    while True:
        schedule.run_pending()
        time.sleep(1)
