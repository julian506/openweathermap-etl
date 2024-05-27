import datetime
from functools import reduce


def extractTemperatureValues(data) -> dict[str, float]:
    return {**data["main"]}


def kelvinToCelsius(temp: float) -> float:
    return round(temp - 273.15, 2)


def convertTemperatureValuesToCelsius(
    temp_values: dict[str, float]
) -> dict[str, float]:
    celsius_temp_values: dict[str, float] = {
        key: kelvinToCelsius(value)
        for key, value in temp_values.items()
        if key.startswith("temp") or key == "feels_like"
    }
    return celsius_temp_values


def addTimestampToData(data, data_utc_datetime) -> dict[str, float | datetime.datetime]:
    data["consulted_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["datetime"] = datetime.datetime.fromtimestamp(data_utc_datetime).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    return data


def transformExtractedData(extracted_data) -> dict[str, float | int | datetime.datetime]:
    temp_values: dict[str, float] = extractTemperatureValues(extracted_data)

    data_utc_datetime: int = extracted_data["dt"]

    celsius_temp_values: dict[str, float] = convertTemperatureValuesToCelsius(
        temp_values
    )

    transformed_temp_values: dict[str, float | datetime.datetime] = addTimestampToData(
        celsius_temp_values, data_utc_datetime
    )

    return transformed_temp_values
