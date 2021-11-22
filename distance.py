#!/usr/bin/env python3

import requests

from utils import get_secret

API_KEY = get_secret('google')

url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=Washington%2C%20DC&destinations=New%20York%20City%2C%20NY&units=imperial&key={API_KEY}"
print(url)
payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
