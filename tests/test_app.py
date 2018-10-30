import unittest

import asynctest
import asyncpg

# from aiohttp import web
from unittest import mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from elixir_rems_proxy.app import init_app, main


# TO DO : test middleware and take mandatory api key into account in 200's and 405's


async def create_db_mock(app):
    """Mock the db connection pool."""
    app['pool'] = asynctest.mock.Mock(asyncpg.create_pool())
    return app


class TestFunctions(unittest.TestCase):
    """Test the functions."""

    def setUp(self):
        """Initialise test case."""
        pass

    def tearDown(self):
        """Clear test case."""
        pass

    # def test_init(self):
    #     """Test init type."""
    #     server = init_app()
    #     self.assertIs(type(server), web.Application)

    @mock.patch('elixir_rems_proxy.app.web')
    def test_main(self, mock_webapp):
        """Test if server will run."""
        main()
        mock_webapp.run_app.assert_called()


class TestEndpoints(AioHTTPTestCase):
    """Test the endpoints."""

    @asynctest.mock.patch('elixir_rems_proxy.app.init_db', side_effect=create_db_mock)
    async def get_application(self, pool_mock):
        """Retrieve web Application for test."""
        return init_app()

    @unittest_run_loop
    async def test_info(self):
        """Test the info endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.api_get'):
            resp = await self.client.request("GET", "/")
        assert 200 == resp.status

    # Find out how to mock user to make the function pass
    # @asynctest.mock.patch('elixir_rems_proxy.app.request')
    # @unittest_run_loop
    # async def test_get_200(self, request):
    #     """Test the get endpoint."""
    #     with asynctest.mock.patch('elixir_rems_proxy.app.api_get', side_effect={"smth": "value"}):
    #         request.match_info['user'] = 'username'
    #         resp = await self.client.request("GET", "/user/username")
    #     assert 200 == resp.status

    # Test POST ...

    @unittest_run_loop
    async def test_get_400(self):
        """Test the get endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.user_get'):
            resp = await self.client.request("GET", "/user/", headers={})
        assert 400 == resp.status

    @unittest_run_loop
    async def test_get_401(self):
        """Test the get endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.user_get'):
            resp = await self.client.request("GET", "/user/", headers={"elixir-api-key": "invalid_key"})
        assert 401 == resp.status

    # 405's disabled: write tests that takes mandatory api key into account

    # @unittest_run_loop
    # async def test_get_405(self):
    #     """Test the get endpoint."""
    #     with asynctest.mock.patch('elixir_rems_proxy.app.api_get'):
    #         resp = await self.client.request("GET", "/user")
    #     assert 405 == resp.status

    # Test PATCH 200

    @unittest_run_loop
    async def test_patch_400(self):
        """Test the get endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.user_patch'):
            resp = await self.client.request("PATCH", "/user/", headers={})
        assert 400 == resp.status

    @unittest_run_loop
    async def test_patch_401(self):
        """Test the get endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.user_patch'):
            resp = await self.client.request("PATCH", "/user/", headers={"elixir-api-key": "invalid_key"})
        assert 401 == resp.status

    # @unittest_run_loop
    # async def test_patch_405(self):
    #     """Test the get endpoint."""
    #     with asynctest.mock.patch('elixir_rems_proxy.app.api_get'):
    #         resp = await self.client.request("PATCH", "/user")
    #     assert 405 == resp.status

    # Test DELETE 200

    @unittest_run_loop
    async def test_delete_400(self):
        """Test the get endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.user_delete', side_effect={"smth": "value"}):
            resp = await self.client.request("DELETE", "/user/", headers={})
        assert 400 == resp.status

    @unittest_run_loop
    async def test_delete_401(self):
        """Test the get endpoint."""
        with asynctest.mock.patch('elixir_rems_proxy.app.user_delete', side_effect={"smth": "value"}):
            resp = await self.client.request("DELETE", "/user/", headers={"elixir-api-key": "invalid_key"})
        assert 401 == resp.status

    # @unittest_run_loop
    # async def test_delete_405(self):
    #     """Test the get endpoint."""
    #     with asynctest.mock.patch('elixir_rems_proxy.app.api_get', side_effect={"smth": "value"}):
    #         resp = await self.client.request("DELETE", "/user")
    #     assert 405 == resp.status


if __name__ == '__main__':
    unittest.main()
