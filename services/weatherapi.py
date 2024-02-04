import requests
import json

class WeatherAPI:

    def __init__(self) -> None:
        self.url = "https://weatherapi-com.p.rapidapi.com/current.json"
        self.headers = {
                    "X-RapidAPI-Key": "427a90fc41msh4ce02db795252e4p149596jsnbd9b123ef525",
	                "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
        }

    def get_weather(self, location):
        querystring = {"q":location}
        response = requests.get(self.url, headers=self.headers, params=querystring)

        return response.json()
    