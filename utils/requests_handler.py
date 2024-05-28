from typing import Any
import requests
from utils import logs
from logging import Logger

logger: Logger = logs.getLogger()


def performRequest(request_url) -> dict[str, Any]:
    try:
        response: requests.Response = requests.get(request_url)
        data: dict[str, Any] = response.json()
        return data
    except:
        raise logs.exceptionLog(f"Error performing request to the URL: {request_url}")
