import requests

ngrok_url = 'https://5b4fa48a9c17.ngrok.io'
endpoint = f'{ngrok_url}/cars'

r =requests.post(endpoint, json={})
print(r.json())