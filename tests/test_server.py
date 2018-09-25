import unittest

from aiohttp.test_utils import AioHTTPTestCase
from aiohttp import web
from proxy.app import init, main
from unittest import mock


class TestFunctions(unittest.TestCase):
    """Test the functions."""

    def setUp(self):
        """Initialise test case."""
        pass

    def tearDown(self):
        """Clear test case."""
        pass

    @mock.patch('proxy.app.web')
    def test_main(self, mock_webapp):
        """Test if server will run."""
        main()
        mock_webapp.run_app.assert_called()

    def test_init(self):
        """Test if init() creates a web app."""
        server = init()
        self.assertIs(type(server), web.Application)


class TestEndpoints(AioHTTPTestCase):
    """Test the endpoints."""

    async def get_application(self):
        """Get the server initialisation."""
        return init()

    async def test_health(self):
        """Test that the server is running."""
        response = await self.client.request("GET", "/health")
        assert response.status == 200

    async def test_api_400_no_headers(self):
        """Test that api returns 400 when all mandatory headers are missing."""
        response = await self.client.request("GET", "/entitlements")
        assert response.status == 400

    async def test_api_400_no_key(self):
        """Test that api returns 400 when one mandatory headers is missing."""
        headers = {'elixir-id': 'user'}
        response = await self.client.request("GET", "/entitlements", headers=headers)
        assert response.status == 400

    async def test_api_400_no_user(self):
        """Test that api returns 400 when one mandatory headers is missing."""
        headers = {'api-key': 'secret'}
        response = await self.client.request("GET", "/entitlements", headers=headers)
        assert response.status == 400

    async def test_api_200(self):
        """Test that api returns 200 when headers are provided."""
        headers = {'api-key': 'secret', 'elixir-id': 'user'}
        response = await self.client.request("GET", "/entitlements", headers=headers)
        assert response.status == 200


if __name__ == '__main__':
    unittest.main()
