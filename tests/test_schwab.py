import unittest
from urllib.parse import parse_qs, unquote, urlparse


class OAuthCodeTests(unittest.TestCase):
    def test_redirect_code_is_decoded_before_token_exchange(self):
        redirected = "https://127.0.0.1/?code=C0.example%40&session=abc"
        code = unquote(parse_qs(urlparse(redirected).query)["code"][0])
        self.assertEqual(code, "C0.example@")
