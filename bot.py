import firebase_admin
from firebase_admin import credentials, db
import requests
import time

# 1. FIREBASE SETUP
service_account_info = {
  "type": "service_account",
  "project_id": "trial-62453",
  "private_key_id": "3c46ee48eaf2d62ea3d0a15278053a7cf1f9ea74",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCq8nHdmig7ozYk\n/Uh+3I+d843l/H2SbhTEcQyun8xxstVKAn8cpcoydrJ7FE6/U/7QHwLr8/oYcJ44\n2C2FG7STc+vtUfQ2xiuxmNRHmC4OBFlY3PdeeX9kuO4jyN8UWTKSL7a/VJBBvc2y\nhT2lScy6nxmnMrmSRDk5rYhzCtn+graaVOfkH2ncuxcWna5K7bLrldBPg5fSe2K1\nslKalBRor2N44UR3uwF1xSmTJFqTWsxK+k03uFJoDy6/A9XSto3ImFk7KD87g4Za\nYSp44CggFZ/zP2NKBT/Xv9qs1pCiD/9b8V1YhX2fC22GL+eX0hj5kwBakJUbgRPU\n51TjzVwXAgMBAAECggEAAitw5sR8PiomV6nsFecyN0wfatM2KAirapPyv4dDxiP3\n+K0U5bSvmhxKQi1FsTaE0wJCXs+bgfn7BkatXsRS6JrRUpNd1Btgfb+uVNZzXQnz\nUqsRxIpRsn+dAFDjLELULemCRqEE8lKCgwtabTfUE1k6JWU82GwQj5EePx/cyeqU\n9HCRwLBF3UlnANIOEQRx3xLmwRC20ZqB1F6LoLEbskQYnCNz5sRfygKdE3ad5Em6\ntt++SecwlmdW4xA5X5eJOAR9R9IbD302J04rSK0XHRr5OnbIYl8TxtYmUEk4qTkD\nkAaDAuHEXFkoH3a5iyUobyXj1h9jw9lOd7z1oBB9qQKBgQDRnlWEoz8o1gmd5gDa\nXZSvyBr1p1M5qE4IDZH97WsXSrYpdrdCJQa8WpZ6vXlL8C/QxVW1YqHUfsbsqSCX\VZ0kV9hFywrsLVaAqv3LStGrD2Y/Zhs05Jc8KV8czprQrlNlci5f4OJoMksE9DnD\ngR7x1aCDeiYh02fPJQ6QK6ox/wKBgQDQxZlRFkdEdtaZkREULhrRsIFn1gISwneU\nyoEKWXt97l6dGGL6+cIyWzojavT9Gbng85k6D79BcUbp+glR1vVkCcBNxSzU/z+c\nHfchRbviGvHShqClsKFsqrgfu6WHu0FxjGpa0sqanYnfSEyMmkEH9k9v6UJwrNJl\nqbzQ21Ql6QKBgQChjhR/C4pMINp8lZ4mrmVALUuJ9RIRqAOr9TmFqYwWAYDv6A1J\nr1vHo1HC+3EW8+EGWHC8QW5UZflOwPLbcCKSthl7gQfECxVWSXMdUWbTHiVBy6JA\nW8Wrmn8xppJvL0wbLatMPfiBMfHbuZcjdMqyvGDftC7bdyHU5syYlO6xZQKBgCv2\nwJ+TynQ/dlemdetC/kDUI5wjNBKRQy9hKaVtTJUrYl9AqG9jsyJ5lZepyWeXSE53\n3fedI1B7s0xIbDgAxXJIn2eBMzyzd8i/grBOCA/ITs5frWrW9Fd26Ak+sdAQfeqU\ngD0aELJYpJURm5UsUq+DjhzqCSTDMBdalDmDRogpAoGAXTJLy5Xie8xv0pFGmVUi\nbFnZQROOGiPShHe2UJ01S8DwClFtoPLbOkmcQpq5KYswmLaLR30+Rx2QFstDVynB\nWvtNqfFzl7URYxFx6NV+HuY6e/T/niCfwSxHZwya8QsW3hZ9uKdkmX3a9zwifBYf\nsT+cwwDN8YJ7WhPW67PkQwI=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@trial-62453.iam.gserviceaccount.com"
}

cred = credentials.Certificate(service_account_info)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://trial-62453-default-rtdb.firebaseio.com'
})

# 2. NSE API CONFIG
headers = {
    "x-rapidapi-key": "b85b401701msh2839e49e0a12876p100141jsn2921f6c682b8",
    "x-rapidapi-host": "nse-stock-market-india.p.rapidapi.com"
}

def update_price():
    url = "https://nse-stock-market-india.p.rapidapi.com/symbol/SBIN"
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if 'lastPrice' in data:
            db.reference('live_stocks/SBIN').update({
                'price': data['lastPrice'],
                'updatedAt': data['lastUpdateTime']
            })
            print(f"Updated SBIN: {data['lastPrice']}")
    except Exception as e:
        print(f"Error: {e}")

# Dar 1 minute bhav update thase (Loop of 5 for safety)
for i in range(5):
    update_price()
    time.sleep(60)

