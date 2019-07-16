import requests

url = "https://scihub.copernicus.eu/apihub/odata/v1/Products"
user = "dsabljak"
passw = "Jabuka!=42"
print('a')
req = requests.get(url, auth=(user, passw), params={'$format': 'json', '$inlinecount': 'allpages', '$top': '1','$filter': 'year(ContentDate/Start) ge 2018' })
#print(req.text)
print(req.status_code)
print(req.json(), file = open('ispis.txt', 'w'))
js = req.json()
a = js['d']['results'][0]['__metadata']['media_src']
a = "https://scihub.copernicus.eu/dhus/odata/v1/Products('4086bab4-857e-4094-b54e-297f5fbc3bfc')/$value"
with open(f"test.zip", "wb") as fout:
            fout.write(requests.get(a,auth=(user, passw)).content)
print(a, file = open('ispis.txt','w'))


