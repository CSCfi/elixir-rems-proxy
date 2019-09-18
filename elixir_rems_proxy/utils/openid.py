"""ELIXIR AAI Requirements for GA4GH RI."""

from ..utils.config import CONFIG
from ..utils.logging import LOG


async def jwks_json(request):
    """Return JWK set keys."""
    LOG.debug('Handle JWK request.')

    data = {
        'keys': [
            CONFIG.public_key
        ]
    }
    # Insert key id and encryption algorithm
    data['keys'][0].update({'kid': CONFIG.key_id})
    data['keys'][0].update({'alg': 'RS256'})

    return data
