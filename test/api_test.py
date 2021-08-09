import pydor.api

import unittest
import requests_mock
import requests
import mock
import json
from os.path import expanduser


class TestApi(unittest.TestCase):
    def test_init(self):
        api = pydor.api.API('localhost:5000')
        self.assertIsInstance(api, pydor.api.API)

    @requests_mock.mock()
    def test_base(self, m):
        api = pydor.api.API('localhost:5000', insecure=True)
        m.get('http://localhost:5000/v2/', text='{}')
        result = api.Base().get()
        self.assertEqual(result.status_code, requests.codes.ok)
        self.assertEqual(result.text, "{}")

    @requests_mock.mock()
    def test_catalog(self, m):
        api = pydor.api.API('localhost:5000', insecure=True)
        m.get('http://localhost:5000/v2/_catalog', text='{"repositories":[]}')
        result = api.Catalog().get()
        self.assertEqual(result.status_code, requests.codes.ok)
        self.assertEqual(result.text, '{"repositories":[]}')

    @requests_mock.mock()
    def test_tags(self, m):
        api = pydor.api.API('localhost:5000', insecure=True)
        m.get('http://localhost:5000/v2/a/tags/list', text='{"name":"a","tags":["latest"]}')
        result = api.Tags("a").get()
        self.assertEqual(result.status_code, requests.codes.ok)
        self.assertEqual(result.text, '{"name":"a","tags":["latest"]}')

    @requests_mock.mock()
    def test_connection_error(self, m):
        api = pydor.api.API('registry.test')
        m.get('https://registry.test/v2/', exc=requests.exceptions.ConnectTimeout)
        with self.assertRaises(requests.exceptions.ConnectTimeout):
            result = api.Base().get()
