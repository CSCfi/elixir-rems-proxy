import unittest

import asynctest

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
from api.app import init_app, main
from unittest import mock


class TestFunctions(unittest.TestCase):
    """Test the functions."""

    def setUp(self):
        """Initialise test case."""
        pass

    def tearDown(self):
        """Clear test case."""
        pass

    async def test_db_pool_init(self):
        """Test opening of db pool."""
        app = {}
        with asynctest.mock.patch('api.app.init_db_pool') as db_mock:
            await init_app(app)
            await db_mock.assert_called()

    async def test_db_pool_close(self):
        """Test closing of db pool."""
        app = {}
        with asynctest.mock.patch('api.app.init_db_pool') as db_mock:
            await init_app(app)
            await db_mock.close.assert_called()

    @mock.patch('api.app.web')
    def test_main(self, mock_webapp):
        """Test if server will run."""
        main()
        mock_webapp.run_app.assert_called()

    def test_init_app(self):
        """Test if init() creates a web app."""
        server = init_app()
        self.assertIs(type(server), web.Application)


class TestEndpoints(AioHTTPTestCase):
    """Test the endpoints."""

    async def get_application(self):
        """Get the server initialisation."""
        return init_app()

    async def test_health(self):
        """Test that the server is running."""
        response = await self.client.request("GET", "/")
        assert response.status == 200
        assert response.text == 'ELIXIR AAI API for REMS'


if __name__ == '__main__':
    unittest.main()
