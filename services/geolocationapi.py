import requests

class LocationAPI():
    
    def __init__(self) -> None:
        self.url = "https://ip-geolocation-ipwhois-io.p.rapidapi.com/json/"
        self.headers = {
                    "X-RapidAPI-Key": "427a90fc41msh4ce02db795252e4p149596jsnbd9b123ef525",
					"X-RapidAPI-Host": "ip-geolocation-ipwhois-io.p.rapidapi.com"
        }

    def get_location(self, ip):
        querystring = {"ip":ip}
        response = requests.get(self.url, headers=self.headers, params=querystring)

        return response.json()