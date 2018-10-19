"""Database Queries."""

from ..utils.logging import LOG


async def user_exists(user, db_pool):
    """Check if user exists."""
    LOG.debug(f'Check if user {user} exists')
    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        # Start a new session with the connection
        async with connection.transaction():
            query = f"""SELECT userid FROM users WHERE userid='{user}';"""
            statement = await connection.prepare(query)
            db_response = await statement.fetch()
            LOG.debug(f'Response: {db_response}')
            return db_response


async def get_dataset_permissions(user, db_pool):
    """Return dataset permissions for given user."""
    LOG.debug(f'Query database for {user}\'s dataset permissions')
    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        # Start a new session with the connection
        async with connection.transaction():
            query = f"""SELECT organization, a.resid, a.start, a.endt
                     FROM resource a, entitlement b
                     WHERE a.id=b.resid
                     AND b.userid='{user}';"""
            statement = await connection.prepare(query)
            db_response = await statement.fetch()
            LOG.debug(f'Response: {db_response}')
            return db_response


async def create_user(user, db_pool):
    """Create new user."""
    LOG.debug(f'Create new user {user}')
    # Take one connection from the active database connection pool
    try:
        async with db_pool.acquire() as connection:
            # Start a new session with the connection
            async with connection.transaction():
                await connection.execute(f"""INSERT INTO users VALUES ($1)""", user)
        return True  # User was created
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to create user -> {e}')
        return False


async def dataset_exists(ds, db_pool):
    """Check if given dataset exists.

    Returns dataset resource id for later use."""
    LOG.debug(f'Check if dataset {ds} exists')
    # Take one connection from the active database connection pool
    async with db_pool.acquire() as connection:
        # Start a new session with the connection
        async with connection.transaction():
            query = f"""SELECT id FROM resource WHERE organization='{ds[0]}' AND resid='{ds[1]}';"""
            statement = await connection.prepare(query)
            db_response = await statement.fetch()
            LOG.debug(f'Response: {db_response}')
            return db_response

async def create_dataset_permissions(dataset_group, db_pool):
    """Create dataset permissions."""
    LOG.debug(datasets)
    # Take one connection from the active database connection pool
    try:
        async with db_pool.acquire() as connection:
            # Start a new session with the connection
            async with connection.transaction():
                for affiliation in dataset_group:
                    
                    # await connection.execute(f"""INSERT INTO users VALUES ($1)""", user)
        return True  # User was created
    except Exception as e:
        LOG.debug(f'An error occurred while attempting to create permissions -> {e}')
        return False
