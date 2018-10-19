"""Process Requests."""

from ..utils.logging import LOG
from ..utils.db_actions import user_exists, create_user
from ..utils.db_actions import get_dataset_permissions, create_dataset_permissions

async def create_response_body(db_response):
    """Construct a dictionary for JSON response body."""
    response_body = {
        "permissions": [
            {
                "affiliation": "",
                "source_signature": "",
                "url_prefix": "",
                "datasets": [dict(item)['resid'] for item in db_response]
            }
        ]
    }
    return response_body


async def process_post_request(request, db_pool):
    """Create new user with dataset permissions."""
    LOG.debug('Process POST request.')
    request_body = await request.json()
    db_response = await user_exists(request_body['user_identifier'], db_pool)
    if db_response:
        # user_identifier exists, new user can't be created
        return 'user_identifier is taken', None
    else:
        # Create new user and dataset permissions
        user_created = await create_user(request_body['user_identifier'], db_pool)
        # Wait for user to be created, then add dataset permissions
        if user_created:
            # Parse datasets out of request_body
            # ELIXIR API Specification has a typo in it, but this iterator satisfies it.
            # Come back and fix this dictionary-array-mess once the specification has been corrected
            dataset_group = [[p['affiliation'], p['datasets']] for p in body['datasets'][0]['permissions']]
            permissions_created = await create_dataset_permissions(dataset_group, db_pool)
            LOG.debug(permissions_created)


async def process_get_request(user, db_pool):
    """Fetch user dataset permissions."""
    LOG.debug('Process GET request.')
    db_response = await user_exists(user, db_pool)
    if db_response:
        permissions = await get_dataset_permissions(user, db_pool)
        if permissions:
            # Return permitted datasets
            permissions_response = await create_response_body(permissions)
            return None, permissions_response
        else:
            # User has no dataset permissions
            return 'Permissions for this user not found', None
    else:
        # User doesn't exist
        return 'User not found', None


async def process_patch_request():
    """Update user's dataset permissions."""
    LOG.debug('Process PATCH request.')
    pass


async def process_delete_request():
    """Delete user and dataset permissions."""
    LOG.debug('Process DELETE request.')
    pass
