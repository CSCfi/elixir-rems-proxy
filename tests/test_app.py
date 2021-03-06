import asynctest

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from elixir_rems_proxy.app import init_app


class TestApp(AioHTTPTestCase):
    """Test functions for the web application."""

    async def get_application(self):
        """Retrieve web app for the tests."""
        return await init_app()

    @unittest_run_loop
    async def test_index(self):
        """Test that the index endpoint works."""
        resp = await self.client.request("GET", "/")
        self.assertEqual(200, resp.status)

    @unittest_run_loop
    async def test_permissions_without_key(self):
        """Test that /permissions requires an api key."""
        resp = await self.client.request("GET", "/permissions/user")
        self.assertEqual(400, resp.status)

    @asynctest.patch("elixir_rems_proxy.app.request_rems_permissions", return_value=[])
    @unittest_run_loop
    async def test_permissions(self, _rems_permissions):
        """Test that /permissions works if api key is provided."""
        resp = await self.client.request("GET", "/permissions/user", headers={"Permissions-Api-Key": "abc"})
        self.assertEqual(200, resp.status)
        # check that a json dict is returned, containing ga4gh passports
        content = await resp.json()
        self.assertIn("ga4gh_passport_v1", content)

    @unittest_run_loop
    async def test_jwks(self):
        """Test that jwks.json works."""
        resp = await self.client.request("GET", "/jwks.json")
        self.assertEqual(200, resp.status)
        # check that a json dict is returned
        content = await resp.json()
        self.assertIsInstance(content, dict)
