"""Process Requests."""

import time
from typing import List, Optional, Tuple

from datetime import datetime
from uuid import uuid4

import aiohttp
import dateutil.parser

from aiohttp import web
from authlib.jose import jwt

from ..config import CONFIG, LOG
from ..utils.types import Permission, Visa, Passport


async def create_ga4gh_visa_v1(permissions: List[Permission]) -> List[Visa]:
    """Construct a GA4GH Passport Visa type of response."""
    LOG.debug("Construct a GA4GH Passport Visa type of response.")

    # Collect permissions here
    visas = []

    for permission in permissions:

        # expires was removed from new RI spec
        # # REMS doesn't have "end" date, for now, replace it with "start" + 3 years for an estimate
        # if permission.get('end') is None:
        #     expires = await iso_to_timestamp(permission.get('start'))
        #     expires += 94608000
        # else:
        #     # Fallback, in case REMS is updated to use this key
        #     expires = await iso_to_timestamp(permission.get('end'))

        visa = {
            "type": "ControlledAccessGrants",
            "value": f'{CONFIG.repository}{permission.get("resource")}',
            "source": "https://ga4gh.org/duri/no_org",
            "by": "dac",
            "asserted": await iso_to_timestamp(permission.get("start")),
        }
        visas.append(Visa(visa))

    return visas


async def iso_to_timestamp(iso: Optional[str]) -> Optional[int]:
    """Convert ISO 8601 date to (int)timestamp without milliseconds.

    2020-01-01T12:00:00.000Z -> 1559893314
    """
    LOG.debug("Convert date to timestamp.")

    # Check that date is not null
    if isinstance(iso, str):
        # Convert ISO 8601 to date
        date = dateutil.parser.parse(iso)
        # Convert date to timestamp
        ts = datetime.timestamp(date)
        # Convert timestamp to string for splitting
        ts_str = str(ts)
        # Split timestamp to remove millis
        ts_split = ts_str.split(".")
        # Convert string to integer
        timestamp_final = int(ts_split[0])
        return timestamp_final
    else:
        return None


async def call_rems_api(url: str, headers: dict) -> List[Permission]:
    """Send request for permissions."""
    LOG.debug("Send request for permissions.")

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                # REMS peculiarity: user not found == user found, but no permissions
                # if result == []:
                #     raise web.HTTPNotFound(text='Request was successful, but no records were found. '
                #                                 'Either the user has no permissions, or the username was not found.')
                return result
            elif response.status == 400:
                LOG.error(f"400: {response}")
                raise web.HTTPBadRequest(text="400 Bad Request")
            elif response.status == 401:
                LOG.error(f"401: {response}")
                raise web.HTTPUnauthorized(text="401 Unauthorized")
            elif response.status == 403:
                LOG.error(f"403: {response}")
                raise web.HTTPForbidden(text="403 Forbidden")
            elif response.status == 404:
                LOG.error(f"404: {response}")
                raise web.HTTPNotFound(text="404 Not Found")
            else:
                LOG.error(f"500: {response}")
                raise web.HTTPInternalServerError(text="500 Internal Server Error")


async def generate_jwt_timestamps() -> Tuple[int, int]:
    """Generate issue and expiry timestamps for JWT."""
    LOG.debug("Generating timestamps for JWT.")

    # Get an epoch base time in seconds (int)
    base_time = str(time.time()).split(".")
    # Issued at
    iat = int(base_time[0])
    # Expires at iat+1h
    exp = iat + CONFIG.jwt_exp

    return iat, exp


async def create_ga4gh_passports(request: web.Request, username: str, visas: List[Visa]) -> List[Passport]:
    """Create GA4GH Passports from GA4GH Visas."""
    LOG.debug("Crafting JWTs.")

    # `jku` and `iss` used to be formed with:
    # f'{request.scheme}://{request.host}/jwks.json'
    # but in openshift containers the apps are http,
    # even though the ingress router is https.
    # Hard-coding these for a quick fix (proxy is temporary)

    # Collect passports here
    passports = []
    header = {
        "jku": f"https://{request.host}/jwks.json",
        "kid": CONFIG.public_key["keys"][0]["kid"],
        "alg": "RS256",
        "typ": "JWT",
    }

    for visa in visas:

        iat, exp = await generate_jwt_timestamps()

        # Prepare the payload for JWT encoding
        payload = {
            "iss": f"https://{request.host}/",
            "sub": username,
            "ga4gh_visa_v1": visa,
            "iat": iat,
            "exp": exp,
            "jti": str(uuid4()),
        }

        # Encode permissions into a JWT
        encoded_visa = jwt.encode(header, payload, CONFIG.private_key).decode("utf-8")
        passports.append(encoded_visa)

    return passports


async def request_rems_permissions(request: web.Request, username: str, api_key: str) -> List[Passport]:
    """Fetch dataset permissions from REMS."""
    LOG.debug("Fetch dataset permissions from REMS.")

    # Items needed for REMS API call
    rems_api = f"{CONFIG.rems_url}?user={username}"
    headers = {"x-rems-api-key": api_key, "x-rems-user-id": username, "content-type": "application/json"}

    # Call the REMS API, request for permissions
    permissions = await call_rems_api(url=rems_api, headers=headers)

    # Check if permissions were retrieved
    if permissions:
        # Parse REMS records into GA4GH passport visas
        ga4gh_visas = await create_ga4gh_visa_v1(permissions)
        # Craft JWT tokens "ga4gh passports" from each permission "visa"
        ga4gh_passports = await create_ga4gh_passports(request, username, ga4gh_visas)
        # Return JWTs
        return ga4gh_passports
    else:
        # Return empty list due to no permissions found
        return []
