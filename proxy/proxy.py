#!/usr/bin/env python3

import aiohttp
import os
import logging

from aiohttp import web

# Logging
FORMAT = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


async def hello(request):
    """Health check."""
    return web.HTTPOk()


async def entitlements(request):
    """
    Request endpoint.

    Required headers:
        api-key (translates to x-rems-api-key)
        elixir-id (translates to x-rems-user-id)
    """
    try:
        api_key = request.headers['api-key']
        try:
            user_id = request.headers['elixir-id']
            async with aiohttp.ClientSession() as session:
                headers = {'User-Agent': 'ELIXIR AAI Entitlements Proxy',
                           'x-rems-api-key': api_key,
                           'x-rems-user-id': user_id}
                LOG.info('Send request to REMS with headers: ' + str(headers))
                async with session.get(os.environ.get('REMS_API_URL', 'http://localhost:3000/api/entitlements'),
                                       ssl=os.environ.get('HTTPS_ONLY', False),
                                       headers=headers) as response:
                    return web.Response(text=await response.text())
        except KeyError as e:
            return web.HTTPBadRequest()
    except KeyError as e:
        return web.HTTPBadRequest()


def main():
    """Run proxy."""
    app = web.Application()
    app.router.add_get('/', hello)
    app.router.add_get('/entitlements', entitlements)
    web.run_app(app,
                host=os.environ.get('APP_HOST', 'localhost'),
                port=os.environ.get('APP_PORT', 5000))


if __name__ == '__main__':
    main()
