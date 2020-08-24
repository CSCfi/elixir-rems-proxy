"""ELIXIR Permissions API proxy for REMS API."""

import sys

from aiohttp import web

from .middlewares import api_key, username_in_path
from .endpoints.permissions import request_rems_permissions
from .config import CONFIG, LOG

routes = web.RouteTableDef()


@routes.get("/", name="index")
async def index(request: web.Request) -> web.Response:
    """Return name of service, doubles as a health check function."""
    LOG.debug("INFO Request received.")
    return web.Response(text="ELIXIR Permissions API proxy for REMS API")


@routes.get("/permissions/{username}")
async def get_permissions(request: web.Request) -> web.Response:
    """GET request to the /permissions endpoint.

    List all datasets user has access to.
    """
    LOG.debug("GET Request received.")

    permissions = await request_rems_permissions(
        request=request, username=request.match_info.get("username"), api_key=request.headers.get("Permissions-Api-Key")
    )

    # The new GA4GH RI format
    ga4gh_passport = {"ga4gh_passport_v1": permissions}

    return web.json_response(ga4gh_passport)


@routes.get("/jwks.json")
async def jwks(request: web.Request) -> web.Response:
    """Return JWK set keys."""
    LOG.info("Received request to GET /jwks.json.")
    return web.json_response(CONFIG.public_key)


def init_app() -> web.Application:
    """Initialise the app."""
    LOG.info("Initialising the server.")
    app = web.Application(middlewares=[api_key(), username_in_path()])
    app.router.add_routes(routes)
    return app


def main():
    """Run the app."""
    LOG.info("Starting server build.")
    web.run_app(init_app(), host=CONFIG.host, port=int(CONFIG.port), shutdown_timeout=0)


if __name__ == "__main__":
    LOG.info("Starting ELIXIR Permissions API proxy for REMS API.")
    if sys.version_info < (3, 6):
        LOG.error("This application requires Python 3.6 or higher version to function.")
        sys.exit(1)
    main()
