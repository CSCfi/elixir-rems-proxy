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
python elixir_rems_proxy/utils/jwks.py
```
The `private_key.json` is used to sign the JWTs (keep this safe), and clients use the `public_key.json` from the `/jwks.json` endpoint to validate the JWTs.

### Configuration
Some options available in [config.ini](elixir_rems_proxy/utils/config.ini).

Environment variables.
```
DEBUG=True
APP_HOST=0.0.0.0
APP_PORT=8080
REMS_URL=https://<rems>/api/entitlements
CONFIG_FILE=/path/to/config.ini
JWK_PUBLIC_KEY_FILE=/path/to/public_key.json
JWK_PRIVATE_KEY_FILE=/path/to/private_key.json
```

### Development Server
Run local web server.
```
python -m elixir_rems_proxy.app
```

### Production Server
TBD
