from dotenv import load_dotenv
import extract, transform, load
import datetime
import schedule
import time


def main():
    load_dotenv()
    current_weather_data = extract.extractCurrentWeatherData()
    print(current_weather_data)
    transformed_weather_data: dict[str, float | datetime.datetime] = (
        transform.transformExtractedData(current_weather_data)
    )
    print(f"The transformed data: \n {transformed_weather_data}")

    print("Connection to azure")
    load.upload_data(transformed_weather_data)


if __name__ == "__main__":
    schedule.every(5).seconds.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
