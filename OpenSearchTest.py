import requests

url = 'https://scihub.copernicus.eu/dhus/search?q=footprint:"Intersects(POLYGON((-4.53%2029.85,26.75%2029.85,26.75%2046.80,-4.53%2046.80,-4.53%2029.85)))"'
user = "dsabljak"
passw = "Jabuka!=42"

req = requests.get(url, auth=(user, passw))
print(req.text, file = open('opensai.txt', 'w'))
print(req.status_code)
req.json()
