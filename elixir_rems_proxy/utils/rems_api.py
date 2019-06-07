"""Process Requests."""

import os
import hashlib
import json

from datetime import datetime

import aiohttp
import dateutil.parser

from aiohttp import web

from ..utils.config import CONFIG
from ..utils.logging import LOG


async def calculate_signature(body):
    """Calculate SHA256 checksum for ga4gh object body."""
    LOG.debug('Calculate SHA256 checksum for ga4gh object body.')

    # Dump python dict into string representation of JSON
    body_json = json.dumps(body)

    # Encode the JSON string to UTF-8 and calculate a SHA256 checksum for it
    hash_object = hashlib.sha256(body_json.encode('utf-8'))
    checksum = hash_object.hexdigest()

    # Add checksum to payload
    body.update({'ga4ghSignature': checksum})

    return body


async def create_response_body(permissions):
    """Construct a dictionary for JSON response body."""
    LOG.debug('Construct a dictionary for JSON response body.')

    # Body base form
    response_body = {
        "ga4gh": {
            "ControlledAccessGrants": [

            ]
        }
    }

    # Append body with permission objects
    for permission in permissions:
        # Missing keys, that are not yet available from REMS and are hardcoded
        # 1. source
        # 2. authoriser
        permission_object = {
            'value': f'https://www.ebi.ac.uk/ega/{permission.get("resource")}',
            'source': 'https://ga4gh.org/duri/no_org',
            'by': 'dac',
            'authoriser': 'rems-demo@csc.fi',
            'asserted': await iso_to_timestamp(permission.get('start')),
            'expires': await iso_to_timestamp(permission.get('end'))
        }
        response_body['ga4gh']['ControlledAccessGrants'].append(permission_object)

    return response_body


async def iso_to_timestamp(iso):
    """Convert ISO 8601 date to (int)timestamp without milliseconds.

    2020-01-01T12:00:00.000Z -> 1559893314"""
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


async def request_rems_permissions(username, api_key):
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
        # Create ga4gh.ControlledAccessGrants payload
        ga4gh_body = await create_response_body(permissions)
        # Calculate SHA256 checksum for contents of ga4gh object
        response_body = await calculate_signature(ga4gh_body)
        # Return permissions object with checksum
        return response_body
    else:
        # Return empty object due to no permissions found
        return {}
