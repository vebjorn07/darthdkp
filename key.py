import jwt
import time
from pathlib import Path

private_key = Path("private_key.pem").read_text()
channel_id = "YOUR_CHANNEL_ID"  # Replace with your channel ID
now = int(time.time())

header = {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "de250eef-03b1-418c-b6ca-94cdc4d58e2b"  # Replace with the "kid" you obtained in step 2
}

payload = {
    "iss": channel_id,
    "sub": channel_id,
    "aud": "https://api.line.me/",
    "exp": now + 1800,  # JWT expires in 30 minutes
    "token_exp": 86400  # Channel access token expires in 1 day
}

encoded_jwt = jwt.encode(payload, private_key, algorithm="RS256", headers=header)

print(encoded_jwt)


import requests

jwt = "JWP: eyJhbGciOiJSUzI1NiIsImtpZCI6ImRlMjUwZWVmLTAzYjEtNDE4Yy1iNmNhLTk0Y2RjNGQ1OGUyYiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJZT1VSX0NIQU5ORUxfSUQiLCJzdWIiOiJZT1VSX0NIQU5ORUxfSUQiLCJhdWQiOiJodHRwczovL2FwaS5saW5lLm1lLyIsImV4cCI6MTY4MjI3MjY3OSwidG9rZW5fZXhwIjo4NjQwMH0.ncW_y5kqNciM_FOsOxAOLkox0J6m7zrtS3-2sbGewENRSSR-uZUvIX9EQdSZ4jGSZTAjxKikOjvhk1aGI42-uFltaEyQKyY1q80Nk5Xa2q8Q15dBR_-mddjOh4dEHBu6gT0Se2zBJmsCVR_1Cbgw12ZikEkPa_dudhaPuD3SwWDlVS10amxSBpk0x05wBI_6vK-0Rv9RpVReGkz66VSI_GIBOeSvupQ5vsKWnNEg9wEkjxR4LsCN4fRiLrDG5qz4VEH3CiOigmx1DRpzXItlgbpZhqJPeH0Ac7qWO20El6eeAvlF9AhJMUOwUSvxpPeAyyLrqWmiVzkNqxrHymKrlw "  # Replace with the JWT you generated earlier

# Step 1: Issue a channel access token
url = "https://api.line.me/v2/oauth/accessToken"
headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": jwt
}

response = requests.post(url, headers=headers, data=data)
response_data = response.json()

# Step 2: Store the channel access token and key ID pair
channel_access_token = response_data["access_token"]
key_id = response_data["key_id"]

# Store the channel_access_token and key_id in your database or another suitable location