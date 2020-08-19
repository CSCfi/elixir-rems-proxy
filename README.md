# ELIXIR Permissions API for REMS
`elixir-rems-proxy` is a proxy web server, which implements the [ELIXIR Permissions API](), by forwarding requests to [REMS]() and returning the responses in [GA4GH Passport]() format.

## Set Up
Download repository and install packages.
```
git clone https://github.com/CSCfi/elixir-rems-proxy.git
cd elixir-rems-proxy
pip install -r requirements.txt
```
Generate JWK set.
```
python elixir_rems_proxy/config/jwks.py
```
The `private_key.json` is used to sign the JWTs (keep this safe), and clients use the `public_key.json` from the `/jwks.json` endpoint to validate the JWTs.

### Configuration
Options available in [config.ini](elixir_rems_proxy/utils/config.ini) can be overwritten with the following environment variables.
```
APP_HOST=0.0.0.0
APP_PORT=8080
REMS_URL=https://<rems>/api/entitlements
GA4GH_REPOSITORY=https://www.ebi.ac.uk/ega/
JWT_EXP=3600
JWK_PUBLIC_KEY_FILE=/path/to/public_key.json
JWK_PRIVATE_KEY_FILE=/path/to/private_key.json
```
Environment variables outside of [config.ini](elixir_rems_proxy/utils/config.ini)
```
DEBUG=True  # increases number of logging messages
CONFIG_FILE=/path/to/config.ini
```

### Development Server
Run local web server.
```
python -m elixir_rems_proxy.app
```

### Production Server
TBD

### Endpoints

#### GET /
Returns name of service, can be used as a health-check endpoint.
```
curl localhost:8080
```
```
ELIXIR Permissions API proxy for REMS API
```
#### GET /permissions/{username}
Returns user's REMS permissions in GA4GH passport format (JWT). Permissions are returned as one token (GA4GH visa / JWT) per permission granted. `Permissions-Api-Key` is forwarded to REMS for validation.
```
curl -H 'Permissions-Api-Key: <api key here>' localhost:8080/permissions/user100
```
```
{
    "ga4gh_passport_v1": [
        "header.payload.signature"
    ]
}
```
#### GET /jwks.json
Returns the JWK set for validating JWTs.
```
curl localhost:8080/jwks.json
```
```
{
    "keys": [
        {
            "kty": "RSA",
            "n": "public key here",
            "e": "AQAB",
            "kid": "key id here",
            "alg": "RS256"
        }
    ]
}
```