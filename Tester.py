import requests

url = "https://scihub.copernicus.eu/apihub/odata/v1/Products"
user = "dsabljak"
passw = "Jabuka!=42"
print('a')
req = requests.get(url, auth=(user, passw), params={'$format': 'json' })
#print(req.text)
print(req.status_code)
#print(req.json(), file = open('ispis.txt', 'w'))
js = req.json()
print(len(js['d']['results'][0]))
print(js['d']['results'][0], file = open('ispis.txt', 'w'))
print(js['d']['results'][0]['ContentGeometry'], file = open('ispis2.txt', 'w'))
h = js['d']['results'][0]['ContentGeometry']
print(h)
##with open(f"test.zip", "wb") as fout:
##            fout.write(requests.get(a,auth=(user, passw)).content)
#print(a, file = open('ispis.txt','w'))


