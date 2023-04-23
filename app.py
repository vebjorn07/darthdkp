import json 
from jwt import jwk


key = jwk.JWK.generate(kty='RSA', alg='RS256', use='sig', size=2048)

private_key = key.export_private()
public_key = key.export_public()

with open("private_key.json", "w") as priv_file:
    json.dump(json.loads(private_key), priv_file, indent=2)

def new_func():
    return open("public_key.json", "w")

with new_func() as pub_file:
    json.dump(json.loads(public_key), pub_file, indent=2)

print("Keys generated and saved as private_key.json and public_key.json")
