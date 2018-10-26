"""Database Queries."""

from ..utils.logging import LOG


async def user_exists(user, connection):
    """Check if user exists."""
    LOG.debug(f'Check if user {user} exists')
    try:
        query = f"""SELECT userid FROM users WHERE userid='{user}';"""
        statement = await connection.prepare(query)
        db_response = await statement.fetch()
        LOG.debug(f'Response: {db_response}')
        return db_response
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to fetch user -> {e}')
        return None


async def get_dataset_permissions(user, connection):
    """Return dataset permissions for given user."""
    LOG.debug(f'Query database for {user}\'s dataset permissions')
    try:
        query = f"""SELECT organization, a.resid, a.start, a.endt
                    FROM resource a, entitlement b
                    WHERE a.id=b.resid
                    AND b.userid='{user}';"""
        statement = await connection.prepare(query)
        db_response = await statement.fetch()
        LOG.debug(f'Response: {db_response}')
        return db_response
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to fetch permissions -> {e}')
        return None


async def create_user(user, connection):
    """Create new user."""
    LOG.debug(f'Create new user {user}')
    try:
        # Make inserts inside of a transaction
        async with connection.transaction():
            await connection.execute(f"""INSERT INTO users VALUES ($1)""", user)
            return True  # User was created
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to create user -> {e}')
        return False


async def get_dataset_index(ds, connection):
    """Check if given dataset exists.

    Returns dataset resource id for later use.
    """
    LOG.debug(f'Check if dataset {ds} exists')
    try:
        query = f"""SELECT id FROM resource WHERE organization='{ds[0]}' AND resid='{ds[1]}';"""
        statement = await connection.prepare(query)
        db_response = await statement.fetch()
        if db_response:
            LOG.debug(f'Response: {db_response}')
            return dict(db_response[0])['id']  # Pass id from record
        else:
            # Could not find dataset belonging to this organisation
            return False
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to fetch dataset index -> {e}')
        return None


async def create_dataset_permissions(user, dataset_group, connection):
    """Create dataset permissions."""
    LOG.debug('Create dataset permissions.')
    errors = []
    try:
        # Make inserts inside of a transaction and commit all at once
        async with connection.transaction():
            for affiliation in dataset_group:
                # aff..[0] = affiliation, aff..[1] = [datasets]
                for dataset in affiliation[1]:
                    dataset_index = await get_dataset_index([affiliation[0], dataset], connection)
                    if dataset_index:
                        # Dataset belonging to given organisation exists, create permissions for user
                        await connection.execute(f"""INSERT INTO entitlement (resid, userid) VALUES ($1, $2)""",
                                                 dataset_index, user)
                    else:
                        # Dataset for this organisation doesn't exist
                        errors.append([affiliation[0], dataset])
            return errors
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to create permissions -> {e}')
        return None


async def remove_dataset_permissions(user, connection):
    """Remove dataset permissions."""
    LOG.debug('Remove dataset permissions.')
    try:
        await connection.execute(f"""DELETE FROM entitlement WHERE userid='{user}'""")
        return True
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to remove permissions -> {e}')
        return None


async def delete_user(user, connection):
    """Remove user."""
    LOG.debug('Delete user.')
    try:
        await connection.execute(f"""DELETE FROM users WHERE userid='{user}'""")
        return True
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to delete user -> {e}')
        return None
