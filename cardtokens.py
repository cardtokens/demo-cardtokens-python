import base64
import uuid
import requests
import json
import rsa

# Constants
BASE_URL = 'https://api.cardtokens.io'
API_KEY = '95f734793a424ea4ae8d9dc0b8c1a4d7'

#
# This is the merchantid created within Cardtokens
#
MERCHANTID = "523ca9d5eb9d4ce0a60b2a3f5eb3119d"

#
# The apikey is required from the menu "settings" in Cardtokens
#
APIKEY = "95f734793a424ea4ae8d9dc0b8c1a4d7"

#
# This is the Cardtokens API endpoint
#
HOST = "https://api.cardtokens.io"

#
#
#
PEMPUBLICKEY = "LS0tLS1CRUdJTiBSU0EgUFVCTElDIEtFWS0tLS0tDQpNSUlDQ2dLQ0FnRUExbXN0TVByRlJWZDhUTUdyWTMyNDJwcTQ2aFlFMFBieXcrTnB0MnRDSjBpRHkrWkxQWWJGDQoydVhOSDVQT2d4aTN0NUhVNjYxVVNBOFg5enk3aklPMDlpOGxRMkdoN1dpejlqZXpFVDBpVmNvUGovSFFrV1N1DQorMDljREhSTmpQMmhpa0hZQTA5SVlzTm96ajd4dHYwTnJxbjZacWZ5amhOS1NrN2RUeUVVQ0xoaEwvTUVFRTZ0DQpBRERVUllvS0hVcWtWaXRwWXNwTUdqaUo2QUFJWVVlYU1DdkZ2cnhaSkFNSW5FbnY3THNhTHVBV21pdzRrOXM5DQozTHUxd2gzcDVuNHVrT2lValFYRnk2b003MzBuWm9vU2R2U2lYUlR2UlFwMDkyZDAzbnY5Zk55cWgwM3ZoM2l5DQpMUmNrdGhWdzZmSU83enhyS2NNemhWaHMrd2hQZW0zOURhU05oSjFrZUx4bzcyaDJIL01FMzRuQzNOSUhCUEhQDQpnU0F4dUNKOUJxdVVFbWJ1d0YxNzR4OUY5SEVibmNGWVRTd1hmS3diN1cxZ0F1U1RlWmhKVXc1eDZ6a3ZUTmRTDQp6NFZoUWNPTnVKMnpqbVV0Z1IrcVdzU2M5SHY3VEZESDlQbCt5NmQxeVJ0Rmp2TmlqeGZQUmo5a1dKbVJvcnBVDQpUTFQxOHZ1OGVvODVpY0tNVjVWaVp0MzB4bGlzVFVOMDJOWkxjNG83TVdraHE1eGhGcXhmZDdTZXZEc1FLa0VpDQp6eVFuL3M5Slk2azJsS1BQbjBNeTVSN1RFa0FkSFVERUlIc09qTXlrZnpwYVdoNldMK2RmRlRFVzE4MFNkRHdXDQpsQVdpa2lhaEVPU0NEZUUySlZMOW4yNjdDMmRzRklkNjVPczJKVjE5anl5b2VGQkhOQm11MFBjQ0F3RUFBUT09DQotLS0tLUVORCBSU0EgUFVCTElDIEtFWS0tLS0tDQo="

# Headers
headers = {
    'x-api-key': API_KEY,
    'x-request-id': str(uuid.uuid4()),
    'Content-Type': 'application/json',
    'User-Agent': 'Cardtokens/1'
}

def create_card_token():
    #
    # End point to create token request
    #
    url = f'{HOST}/api/token'

    #
    # The test PAN to generate a test-token of
    #
    card = {
        "pan": "5555341244441115",
        "expmonth": 12,
        "expyear": 2029,
        "securitycode": "000"
    }

    #
    # Convert object to JSON string
    #
    json_card = json.dumps(card)

    #
    # Convert JSON string to bytes
    #
    json_bytes = json_card.encode('utf-8')

    #
    # Decode the string
    #
    decoded_pem_key_bytes = base64.b64decode(PEMPUBLICKEY)

    #
    # Load the public key
    #
    pubkey = rsa.PublicKey.load_pkcs1(decoded_pem_key_bytes.decode('utf-8'))

    #
    # Encrypt the message
    #
    encrypted_card = rsa.encrypt(json_bytes, pubkey)
    
    #
    # Generate the payload request
    #
    payload = {
        "enccard": base64.b64encode(encrypted_card).decode('utf-8'),
	    "clientwalletaccountemailaddress": "noreply@cardtokens.io",
	    "merchantid": MERCHANTID
    }

    #
    # Generate unique request id
    #
    headers["x-request-id"] = str(uuid.uuid4())

    #
    # Request Cardtokens and return the JSON
    #
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def get_card_token(tokenid):
    #
    # Endpoint to get token status
    #
    url = f'{HOST}/api/token/{tokenid}/status'

    #
    # Generate unique request id
    #
    headers["x-request-id"] = str(uuid.uuid4())

    #
    # Request Cardtokens
    #
    response = requests.get(url, headers=headers)

    #
    # Return the response json
    #
    return response.json()

def get_cryptogram(tokenid):
    #
    # Cardtokens cryptogram endpoints
    #
    url = f'{BASE_URL}/api/token/{tokenid}/cryptogram'
    #
    # Generate the payload request
    #
    payload = {
        "reference": "test-cryptogram",
	    "transactiontype": "ecom",
	    "unpredictablenumber": "12345678"
    }

    #
    # Generate unique request id
    #
    headers["x-request-id"] = str(uuid.uuid4())

    #
    # Request the cryptogram
    #
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def delete_token(tokenid):
    #
    # URL to the delete endpoint
    #
    url = f'{BASE_URL}/api/token/{tokenid}/delete'

    #
    # Generate unique request id
    #
    headers["x-request-id"] = str(uuid.uuid4())

    #
    # Request Cardtokens
    #
    response = requests.delete(url, headers=headers)

    #
    # Return the status code. On success = 200
    #
    return response.status_code

#
# Create the token
#
card_token = create_card_token()
print(card_token)
tokenid = card_token['tokenid']
token = card_token['token']
if len(token) == 0:
    raise ValueError("Network token is 0 long")

#
# Get token status
#
tokendata= get_card_token(tokenid)
print(tokendata)

#
# If token status is NOT active - then fail
#
status = tokendata["status"]
if status != "ACTIVE":
    raise ValueError("Status is not ACTIVE")

#
# Fetch a cryptogram
#
cryptogramdata = get_cryptogram(tokenid)
print(cryptogramdata)

#
# Validate that the cryptogram has a value
#
cryptogram = cryptogramdata["cryptogram"]
if len(cryptogram) == 0:
    raise ValueError("Cryptogram is 0 long")

#
# Delete the token
#
statuscode = delete_token(tokenid)
if statuscode != 200:
    raise ValueError("Could not delete the token!")
