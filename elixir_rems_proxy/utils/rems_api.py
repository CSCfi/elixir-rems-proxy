"""Process Requests."""

from aiohttp import web

from ..utils.config import CONFIG
from ..utils.logging import LOG


async def calculate_signature(body):
    """Calculate SHA256 checksum for ga4gh object body."""
    LOG.debug('Calculate SHA256 checksum for ga4gh object body.')


async def create_response_body(db_response):
    """Construct a dictionary for JSON response body."""
    LOG.debug('Construct a dictionary for JSON response body.')
    response_body = {}
    return response_body


async def request_rems_permissions(username):
    """Fetch dataset permissions from REMS."""
    LOG.debug('Fetch dataset permissions from REMS.')

    # export REMS_URL=http://86.50.169.120:3000/api/entitlements
    # os.environ.get('REMS_URL', CONFIG.rems_url)
