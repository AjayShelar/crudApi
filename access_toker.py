import requests
import base64


url = "https://passbird-api.auth.ap-south-1.amazoncognito.com/oauth2/token"

client_id = "2qo44rlcfsvaf8gshcqqtnvlei"
client_secret_id = "mqfhnnvuork1mqr0vgd0a91t13hl6laelo4de8csm38tufksqpg"

basic = base64.b64encode((client_id+':'+client_secret_id).encode())

payload = 'grant_type=client_credentials&scope=passBirdAppProd/read'
headers = {
    'Authorization': 'Basic '+basic.decode(),
    'Content-Type': 'application/x-www-form-urlencoded',

}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())