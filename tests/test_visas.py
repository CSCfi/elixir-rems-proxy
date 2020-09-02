import aiohttp
import asynctest  # TODO require
import random

from authlib.jose import jwt
from asynctest import CoroutineMock
from unittest.mock import patch

from elixir_rems_proxy.config import CONFIG
from elixir_rems_proxy.endpoints.permissions import create_ga4gh_visa_v1, create_ga4gh_passports, iso_to_timestamp, call_rems_api
import elixir_rems_proxy.endpoints.permissions


class TestBasicFunctions(asynctest.TestCase):
    """Test functions for generation passports and visas."""

    @patch("elixir_rems_proxy.endpoints.permissions.iso_to_timestamp", return_value="")
    async def test_ga4gh_visa(self, _iso_to_timestamp):
        """Test visa generation."""
        # Test that you get as many items in your visa as the input permissions.
        length = random.randint(1, 10)
        visas = await create_ga4gh_visa_v1([{"start": 1} for x in range(length)])
        self.assertEqual(length, len(visas), msg=f"Unequal length for input {length}")

        # Test that the first one contains all fields.
        self.assertIn("type", visas[0])
        self.assertIn("value", visas[0])
        self.assertIn("source", visas[0])
        self.assertIn("by", visas[0])
        self.assertIn("asserted", visas[0])

    async def test_ga4gh_passports(self):
        """Test passport generation."""
        length = random.randint(1, 10)
        visas = "v" * length
        user = "testuser"

        class Request:
            host = "dummyhost"

        passport = await create_ga4gh_passports(Request(), user, visas)
        # Check the length of the passport (number of visas)
        self.assertEqual(length, len(passport), msg=f"Unequal length for input {length}")

        # Check that the first visa can be decoded
        visa = passport[0]
        decoded = jwt.decode(visa, CONFIG.public_key)
        # Check that the first visa contains the correct fields
        self.assertIn("iss", decoded)
        self.assertIn("sub", decoded)
        self.assertIn("ga4gh_visa_v1", decoded)
        # Check that the first visa contains the correct username
        self.assertEqual(decoded["sub"], user)

    async def test_iso_to_timestamp(self):
        """Test that timestamp generation works as expected."""
        iso = "2020-01-01T12:00:00.000Z"
        expected_stamp = 1577880000  # TODO not as in docstring (should it be?)
        stamp = await iso_to_timestamp(iso)
        self.assertEqual(stamp, expected_stamp)

    async def test_generate_jtw_timestamp(self):
        """Test that the expires time is in the future."""
        iat, exp = await elixir_rems_proxy.endpoints.permissions.generate_jwt_timestamps()
        self.assertLess(iat, exp)

    @asynctest.patch("aiohttp.ClientSession.get")
    async def test_call_api_ok(self, session_mock):
        """Test that a successfull call to the rems api."""

        session_mock.return_value.__aenter__.return_value.json = CoroutineMock(side_effect=[{"test": "test"}])
        session_mock.return_value.__aenter__.return_value.status = 200

        res = await call_rems_api("url", {})
        # if successfull, the json response should be returned without changes
        self.assertEqual(res, {"test": "test"})

    @asynctest.patch("aiohttp.ClientSession.get")
    async def test_call_api_fail(self, session_mock):
        """Test that an unsuccessfull call to the rems api."""

        session_mock.return_value.__aenter__.return_value.status = 400
        # status code 400 should raise bad request
        with self.assertRaises(aiohttp.web_exceptions.HTTPBadRequest) as cm:
            await call_rems_api("url", {})
        self.assertEqual(cm.exception.status, 400)

    @asynctest.patch("aiohttp.ClientSession.get")
    async def test_call_api_error(self, session_mock):
        """Test that an unsuccessfull call to the rems api."""

        session_mock.return_value.__aenter__.return_value.status = 500
        # status code 400 should internal server error
        with self.assertRaises(aiohttp.web_exceptions.HTTPInternalServerError) as cm:
            await call_rems_api("url", {})
        self.assertEqual(cm.exception.status, 500)

    @asynctest.patch("elixir_rems_proxy.endpoints.permissions.create_ga4gh_visa_v1")
    @asynctest.patch("elixir_rems_proxy.endpoints.permissions.create_ga4gh_passports")
    @asynctest.patch("elixir_rems_proxy.endpoints.permissions.call_rems_api")
    async def test_request_empty_permissions(self, mock_call_api, _mock_passport, _mock_visa):
        """Test that no passports are returned if no permissions are given."""

        mock_call_api.return_value = []
        passports = await elixir_rems_proxy.endpoints.permissions.request_rems_permissions("", "", "")
        self.assertEqual(passports, [])

    @asynctest.patch("elixir_rems_proxy.endpoints.permissions.create_ga4gh_visa_v1")
    @asynctest.patch("elixir_rems_proxy.endpoints.permissions.create_ga4gh_passports")
    @asynctest.patch("elixir_rems_proxy.endpoints.permissions.call_rems_api")
    async def test_request_permissions(self, mock_call_api, _mock_passport, _mock_visa):
        """Test permission requests."""

        mock_call_api.return_value = ["test"]
        passports = await elixir_rems_proxy.endpoints.permissions.request_rems_permissions("", "", "")
        self.assertNotEqual(passports, [])


if __name__ == "__main__":
    asynctest.main()
