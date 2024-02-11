import requests


#json_data = {'quest':'what are you doing'}
url = "https://92fa-35-240-191-203.ngrok-free.app/data"
headers = {"Content-Type": "application/json"}
#print(json_data)
#response = requests.post(url,json=json_data)

#print(response.text)

while True:
    prompt=input('enter questions >>')
    json_data = {"quest": prompt}
    response = requests.post(url, json=json_data)
    print(f'ai >>{response.text}')
