"""Process Requests."""

from ..utils.logging import LOG
from ..utils.db_actions import user_exists, create_user, delete_user
from ..utils.db_actions import get_dataset_permissions, create_dataset_permissions, remove_dataset_permissions


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
    # Put the JSON payload body into a dictionary object
    request_body = await request.json()

    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        # Check if any users with given name already exist
        user_found = await user_exists(request_body['user_identifier'], connection)
        if user_found:
            # user_identifier exists, new user can't be created
            return 'Username is taken', False
        else:
            # Create new user and dataset permissions
            user_created = await create_user(request_body['user_identifier'], connection)
            # Wait for user to be created, then add dataset permissions
            if user_created:
                # Parse datasets out of request_body
                # ELIXIR API Specification has a typo in it, but this iterator satisfies it.
                # Come back and fix this once the specification has been corrected
                # dataset_group = [[p['affiliation'], p['datasets']] for p in body['permissions']]  # Correct form
                dataset_group = [[p['affiliation'], p['datasets']] for p in request_body['datasets'][0]['permissions']]
                permissions_errors = await create_dataset_permissions(request_body['user_identifier'], dataset_group, connection)
                LOG.debug(f'Error list from creating permissions: {permissions_errors}. Should be empty!')
                if permissions_errors:
                    # If there are errors, return proper message
                    return permissions_errors, True
                else:
                    # All inserts were processed successfully
                    return None, True


async def process_get_request(user, db_pool):
    """Fetch user dataset permissions."""
    LOG.debug('Process GET request.')

    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        # Check if any users with given name already exist
        user_found = await user_exists(user, connection)
        if user_found:
            # User was found, fetch permissions
            permissions = await get_dataset_permissions(user, connection)
            if permissions:
                # Return permitted datasets
                permissions_response = await create_response_body(permissions)
                return None, permissions_response
            else:
                # User has no dataset permissions
                return 'Permissions for this user not found', False
        else:
            # User doesn't exist
            return 'User not found', False


async def process_patch_request(user, request, db_pool):
    """Update user's dataset permissions."""
    LOG.debug('Process PATCH request.')
    # Put the JSON payload body into a dictionary object
    request_body = await request.json()

    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        user_found = await user_exists(user, connection)
        if user_found:
            # user_identifier exists, continue with operations
            # Check if user has permissions to be removed
            permissions = await get_dataset_permissions(user, connection)
            if permissions:
                # Try to remove permissions before adding new permissions
                await remove_dataset_permissions(user, connection)
            # Parse datasets out of request_body
            # ELIXIR API Specification has a typo in it, but this iterator satisfies it.
            # Come back and fix this once the specification has been corrected
            # dataset_group = [[p['affiliation'], p['datasets']] for p in body['permissions']]  # Correct form
            dataset_group = [[p['affiliation'], p['datasets']] for p in request_body['datasets'][0]['permissions']]
            if dataset_group:
                # If any datasets were listed, add permissions for them
                permissions_errors = await create_dataset_permissions(user, dataset_group, connection)
                LOG.debug(f'Error list from creating permissions: {permissions_errors}. Should be empty!')
                if permissions_errors:
                    # If there are errors, return proper message
                    return permissions_errors, True
                else:
                    # All inserts were processed successfully
                    return None, True
            else:
                # Body contained no datasets, end operations here (permissions removed, none added)
                return None, True
        else:
            return 'User not found', False


async def process_delete_request(user, db_pool):
    """Fetch user dataset permissions."""
    LOG.debug('Process GET request.')

    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        user_found = await user_exists(user, connection)
        if user_found:
            # Check if user has permissions to be removed
            permissions = await get_dataset_permissions(user, connection)
            if permissions:
                # Try to remove permissions before removing user
                await remove_dataset_permissions(user, connection)
            # Finally remove the user
            user_removed = await delete_user(user, connection)
            if user_removed:
                return None, True
            else:
                return 'Database error when attempting to remove user', False
        else:
            # User doesn't exist
            return 'User not found', False
