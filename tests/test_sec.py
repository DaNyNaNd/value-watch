import unittest

from value_watch.sec import SEC_HEADERS


class SecRequestTests(unittest.TestCase):
    def test_standard_library_client_does_not_request_unsupported_compression(self):
        self.assertNotIn("Accept-Encoding", SEC_HEADERS)
