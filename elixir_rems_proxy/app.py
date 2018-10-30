"""ELIXIR AAI API for REMS."""

import os
import sys

from aiohttp import web

from .schemas import load_schema
from .utils.validate import validate, api_key, check_user
from .utils.db_pool import init_db_pool
from .utils.process import process_post_request, process_get_request, process_patch_request, process_delete_request
from .utils.logging import LOG

routes = web.RouteTableDef()


@routes.get('/', name='index')
async def api_get(request):
    """Return name of service, doubles as a health check function."""
    LOG.debug('INFO Request received.')
    return web.Response(text='ELIXIR AAI API for REMS')


@routes.post('/user')
@validate(load_schema("post"))
async def user_post(request):
    """POST request to the /user endpoint.

    Create new user with access to given datasets.
    """
    LOG.debug('POST Request received.')
    db_pool = request.app['pool']

    missing_datasets = await process_post_request(request, db_pool)

    if len(missing_datasets) == 0:
        return web.HTTPOk(text='Successful operation')
    else:
        return web.HTTPCreated(text=f'Following datasets are missing from REMS ({missing_datasets}), check "GET /user" endpoint for added permissions')


@routes.get('/user/')
@routes.get('/user/{user}')
async def user_get(request):
    """GET request to the /user endpoint.

    List all datasets user has access to.
    """
    LOG.debug('GET Request received.')
    user_identifier = None  # username in REMS
    db_pool = request.app['pool']

    # try:
    #     # Optional query parameter, retrieved from /user/{user}?user_affiliation={organisation}
    #     # user_affiliation = request.query['user_affiliation']  # NOT IN USE
    # except KeyError as key_error:
    #     LOG.debug(f'KeyError at optional key {key_error}, ignore and pass.')
    #     pass

    if 'user' in request.match_info:
        user_identifier = request.match_info['user']
        processed_request = await process_get_request(user_identifier, db_pool)
        if processed_request:
            return web.json_response(processed_request)
    else:
        raise web.HTTPBadRequest(text='Username not provided')


@routes.patch('/user/')
@routes.patch('/user/{user}')
@validate(load_schema("patch"))
async def user_patch(request):
    """PATCH request to the /user endpoint.

    Update dataset permissions for given user.
    """
    LOG.debug('PATCH Request received.')
    db_pool = request.app['pool']

    if 'user' in request.match_info:
        user_identifier = request.match_info['user']
        processed_request = await process_patch_request(user_identifier, request, db_pool)
        if len(processed_request) == 0 or processed_request is True:
            return web.HTTPOk(text='Successful operation')
        else:
            return web.HTTPCreated(text=f'Following datasets are missing from REMS ({processed_request}), check "GET /user" endpoint for permissions')
    else:
        raise web.HTTPBadRequest(text='Username not provided')


@routes.delete('/user/')
@routes.delete('/user/{user}')
async def user_delete(request):
    """DELETE request to the /user endpoint.

    Delete user.
    """
    LOG.debug('DELETE Request received.')
    user_identifier = None  # username in REMS
    db_pool = request.app['pool']

    if 'user' in request.match_info:
        user_identifier = request.match_info['user']
        await process_delete_request(user_identifier, db_pool)
        return web.HTTPOk(text='User was deleted')
    else:
        raise web.HTTPBadRequest(text='Username not provided')


async def init_db(app):
    """Initialise a database connection pool with the web server."""
    LOG.info('Create PostgreSQL connection pool.')
    app['pool'] = await init_db_pool()


async def close_db(app):
    """Close the database connection pool when server is shut down."""
    LOG.info('Close PostgreSQL connection pool.')
    await app['pool'].close()


def init_app():
    """Initialise the app."""
    LOG.info('Initialise the server.')
    app = web.Application(middlewares=[api_key(), check_user()])
    app.router.add_routes(routes)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app


def main():
    """Run the app."""
    LOG.info('Start server build.')
    web.run_app(init_app(),
                host=os.environ.get('APP_HOST', '0.0.0.0'),
                port=os.environ.get('APP_PORT', '8080'),
                shutdown_timeout=0)


if __name__ == '__main__':
    assert sys.version_info >= (3, 6), "This service requires python3.6"
    LOG.info('Starting server start-up routines.')
    main()
