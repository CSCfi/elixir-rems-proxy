"""Configure Database Connection."""

import os
import asyncpg

POSTGRES = {
    'user': os.environ.get('DB_USER', 'rems'),
    'password': os.environ.get('DB_PASS', 'rems'),
    'database': os.environ.get('DB_NAME', 'rems'),
    'host': os.environ.get('DB_HOST', 'postgresql://localhost:5432').split('/')[2]
}

DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES['user'],
                                                      pw=POSTGRES['password'],
                                                      url=POSTGRES['host'],
                                                      db=POSTGRES['database'])


async def init_db_pool():
    """Create a database connection pool."""
    return await asyncpg.create_pool(dsn=DB_URL)
