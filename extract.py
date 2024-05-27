import requests
import os


def getCoordinatesByZipCode(API_BASE_URL: str, API_KEY: str) -> dict[str, int]:
    ZIP_CODE: str | None = os.getenv("ZIP_CODE")
    COUNTRY_CODE: str | None = os.getenv("COUNTRY_CODE")
    request_url: str = (
        f"{API_BASE_URL}/geo/1.0/zip?zip={ZIP_CODE},{COUNTRY_CODE}&appid={API_KEY}"
    )
    response: requests.Response = requests.get(request_url)
    data: dict = response.json()
    print(f'Identified city: {data["name"]}')
    coordinates: dict[str, int] = {"latitude": data["lat"], "longitude": data["lon"]}
    return coordinates


def extractCurrentWeatherData() -> dict:
    API_BASE_URL: str | None = os.getenv("API_BASE_URL")
    if API_BASE_URL == None:
        raise Exception("API_BASE_URL can't be empty")
    API_KEY: str | None = os.getenv("API_KEY")
    if API_KEY == None:
        raise Exception("API_KEY can't be empty")
    coordinates: dict[str, int] = getCoordinatesByZipCode(API_BASE_URL, API_KEY)
    LATITUDE: int = coordinates["latitude"]
    LONGITUDE: int = coordinates["longitude"]
    request_url: str = (
        f"{API_BASE_URL}/data/2.5/weather?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}"
    )
    response: requests.Response = requests.get(request_url)
    return response.json()
