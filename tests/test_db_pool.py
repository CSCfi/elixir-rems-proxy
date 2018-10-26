# import unittest

# import asynctest

# from elixir_rems_proxy.utils.db_pool import init_db_pool


# class TestFunctions(unittest.TestCase):
#     """Test the functions."""

#     def setUp(self):
#         """Initialise test case."""
#         pass

#     def tearDown(self):
#         """Clear test case."""
#         pass

#     @asynctest.mock.patch('elixir_rems_proxy.utils.db_pool.asyncpg')
#     async def test_init_pool(self, db_mock):
#         """Test database connection pool creation."""
#         db_mock.return_value = asynctest.CoroutineMock(name='create_pool')
#         db_mock.create_pool = asynctest.CoroutineMock()
#         await init_db_pool()
#         db_mock.create_pool.assert_called()


# if __name__ == '__main__':
#     unittest.main()
