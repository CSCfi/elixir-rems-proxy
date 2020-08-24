"""Web Server Middleware Components."""

from typing import Callable

from aiohttp import web

from ..config import LOG


def api_key() -> Callable:
    """Check that user has supplied an api key."""
    LOG.debug("Check that user has supplied an api key.")

    @web.middleware
    async def api_key_middleware(request: web.Request, handler: Callable) -> Callable:
        if "/permissions" in request.path and "Permissions-Api-Key" in request.headers:
            LOG.debug("In /permissions path with api key.")
        elif "/permissions" not in request.path:
            # At index '/' endpoint
            LOG.debug("No API key authentication required at index endpoint")
        else:
            LOG.debug('Missing "Permissions-Api-Key" from headers.')
            raise web.HTTPBadRequest(text="Missing mandatory headers: 'Permissions-Api-Key'")

        # Carry on with request if no exceptions were raised
        return await handler(request)

    return api_key_middleware


def username_in_path() -> Callable:
    """Check that request contains username."""
    LOG.debug("Check that request contains username.")

    @web.middleware
    async def username_in_path_middleware(request: web.Request, handler: Callable) -> Callable:
        if request.path.startswith("/permissions"):
            LOG.debug("Request to permissions endpoint, username must be supplied.")
            if "username" not in request.match_info:
                raise web.HTTPBadRequest(text="Username not provided.")
        else:
            LOG.debug("Username is not required at this endpoint.")

        # Carry on with request if no exceptions were raised
        return await handler(request)

    return username_in_path_middleware
