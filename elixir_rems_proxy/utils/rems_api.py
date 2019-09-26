"""Process Requests."""

import os
import time

from datetime import datetime

import aiohttp
import dateutil.parser

from aiohttp import web
from authlib.jose import jwt

from ..utils.config import CONFIG
from ..utils.logging import LOG


async def create_ga4gh_visa_v1(permissions):
    """Construct a GA4GH Passport Visa type of response."""
    LOG.debug('Construct a GA4GH Passport Visa type of response.')

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
            'type': 'ControlledAccessGrants',
            'value': f'https://www.ebi.ac.uk/ega/{permission.get("resource")}',
            'source': 'https://ga4gh.org/duri/no_org',
            'by': 'dac',
            'asserted': await iso_to_timestamp(permission.get('start')),
        }
        visas.append(visa)

    return visas


async def iso_to_timestamp(iso):
    """Convert ISO 8601 date to (int)timestamp without milliseconds.

    2020-01-01T12:00:00.000Z -> 1559893314
    """
    LOG.debug('Convert date to timestamp.')

    # Check that date is not null
    if isinstance(iso, str):
        # Convert ISO 8601 to date
        date = dateutil.parser.parse(iso)
        # Convert date to timestamp
        ts = datetime.timestamp(date)
        # Convert timestamp to string for splitting
        ts_str = str(ts)
        # Split timestamp to remove millis
        ts_split = ts_str.split('.')
        # Convert string to integer
        timestamp_final = int(ts_split[0])
        return timestamp_final
    else:
        return None


async def call_rems_api(url, headers):
    """Send request for permissions."""
    LOG.debug('Send request for permissions.')

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
                LOG.error(f'400: {response}')
                raise web.HTTPBadRequest(text='400 Bad Request')
            elif response.status == 401:
                LOG.error(f'401: {response}')
                raise web.HTTPUnauthorized(text='401 Unauthorized')
            elif response.status == 403:
                LOG.error(f'403: {response}')
                raise web.HTTPForbidden(text='403 Forbidden')
            elif response.status == 404:
                LOG.error(f'404: {response}')
                raise web.HTTPNotFound(text='404 Not Found')
            else:
                LOG.error(f'500: {response}')
                raise web.HTTPInternalServerError(text='500 Internal Server Error')


async def generate_jwt_timestamps():
    """Generate issue and expiry timestamps for JWT."""
    LOG.debug('Generating timestamps for JWT.')

    # Get an epoch base time in seconds (int)
    base_time = str(time.time())
    base_time = base_time.split('.')
    # Issued at
    iat = int(base_time[0])
    # Expires at iat+1h
    exp = iat + 3600

    return iat, exp


async def create_ga4gh_passports(request, username, visas):
    """Create GA4GH Passports from GA4GH Visas."""
    LOG.debug('Crafting JWTs.')

    # Collect passports here
    passports = []
    header = {
        'jku': f'{request.scheme}://{request.host}/jwks.json',
        'kid': CONFIG.key_id,
        'alg': 'RS256',
        'typ': 'JWT'
    }

    for visa in visas:

        iat, exp = await generate_jwt_timestamps()

        # Prepare the payload for JWT encoding
        payload = {
            'iss': f'{request.scheme}://{request.host}/',
            'sub': username,
            'ga4gh_visa_v1': visa,
            'iat': iat,
            'exp': exp
        }

        # Encode permissions into a JWT
        encoded_visa = jwt.encode(header, payload, CONFIG.private_key).decode('utf-8')
        passports.append(encoded_visa)

    return passports


async def request_rems_permissions(request, username, api_key):
    """Fetch dataset permissions from REMS."""
    LOG.debug('Fetch dataset permissions from REMS.')

    # Items needed for REMS API call
    rems_api = os.environ.get('REMS_URL', CONFIG.rems_url)
    headers = {'x-rems-api-key': api_key,
               'x-rems-user-id': username,
               'content-type': 'application/json'}

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
