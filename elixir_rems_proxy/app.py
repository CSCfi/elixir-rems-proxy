"""ELIXIR Permissions API proxy for REMS API."""

import os
import sys

from aiohttp import web

from .utils.middlewares import api_key, username_in_path
from .utils.rems_api import request_rems_permissions
from .utils.config import CONFIG
from .utils.logging import LOG

routes = web.RouteTableDef()


@routes.get('/', name='index')
async def index(request):
    """Return name of service, doubles as a health check function."""
    LOG.debug('INFO Request received.')
    return web.Response(text='ELIXIR Permissions API proxy for REMS API')


@routes.get('/permissions')
@routes.get('/permissions/')
@routes.get('/permissions/{username}')
async def get_permissions(request):
    """GET request to the /permissions endpoint.

    List all datasets user has access to.
    """
    LOG.debug('GET Request received.')

    permissions = await request_rems_permissions(username=request.match_info.get('username'),
                                                 api_key=request.headers.get('Permissions-Api-Key'))

    return web.json_response(permissions)


def init_app():
    """Initialise the app."""
    LOG.info('Initialising the server.')
    app = web.Application(middlewares=[api_key(), username_in_path()])
    app.router.add_routes(routes)
    return app


def main():
    """Run the app."""
    LOG.info('Starting server build.')
    web.run_app(init_app(),
                host=os.environ.get('APP_HOST', CONFIG.host),
                port=int(os.environ.get('APP_PORT', CONFIG.port)),
                shutdown_timeout=0)


if __name__ == '__main__':
    LOG.info('Starting ELIXIR Permissions API proxy for REMS API.')
    if sys.version_info < (3, 6):
        LOG.error("This application requires Python 3.6 or higher version to function.")
        sys.exit(1)
    main()
