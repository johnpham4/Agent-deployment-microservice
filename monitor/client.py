from time import sleep
import requests
from loguru import logger

def predict():
    logger.info("Sending GET requests!")
    response = requests.get(
        "http://localhost:8000/",
        headers={
            "accept": "application/json",
        },
    )
    print(response.json())

if __name__ == "__main__":
    while True:
        predict()
        sleep(0.5)