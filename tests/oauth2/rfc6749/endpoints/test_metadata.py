# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from oauthlib.oauth2 import MetadataEndpoint
from oauthlib.oauth2 import TokenEndpoint

from ....unittest import TestCase


class MetadataEndpointTest(TestCase):
    def setUp(self):
        self.metadata = {
            "issuer": 'https://foo.bar'
        }

    def test_openid_oauth2_preconfigured(self):
        default_claims = {
            "issuer": 'https://foo.bar',
            "authorization_endpoint": "https://foo.bar/authorize",
            "revocation_endpoint": "https://foo.bar/revoke",
            "introspection_endpoint": "https://foo.bar/introspect",
            "token_endpoint": "https://foo.bar/token"
        }
        from oauthlib.oauth2 import Server as OAuth2Server
        from oauthlib.openid import Server as OpenIDServer

        endpoint = OAuth2Server(None)
        metadata = MetadataEndpoint([endpoint], default_claims)
        oauth2_claims = metadata.claims

        endpoint = OpenIDServer(None)
        metadata = MetadataEndpoint([endpoint], default_claims)
        openid_claims = metadata.claims

        # Pure OAuth2 Authorization Metadata are similar with OpenID but
        # response_type not! (OIDC contains "id_token" and hybrid flows)
        del oauth2_claims['response_types_supported']
        del openid_claims['response_types_supported']

        self.maxDiff = None
        self.assertEqual(openid_claims, oauth2_claims)

    def test_token_endpoint(self):
        endpoint = TokenEndpoint(None, None, grant_types={"password": None})
        metadata = MetadataEndpoint([endpoint], {
            "issuer": 'https://foo.bar',
            "token_endpoint": "https://foo.bar/token"
        })
        self.assertIn("grant_types_supported", metadata.claims)
        self.assertEqual(metadata.claims["grant_types_supported"], ["password"])

    def test_token_endpoint_overridden(self):
        endpoint = TokenEndpoint(None, None, grant_types={"password": None})
        metadata = MetadataEndpoint([endpoint], {
            "issuer": 'https://foo.bar',
            "token_endpoint": "https://foo.bar/token",
            "grant_types_supported": ["pass_word_special_provider"]
        })
        self.assertIn("grant_types_supported", metadata.claims)
        self.assertEqual(metadata.claims["grant_types_supported"], ["pass_word_special_provider"])

    def test_mandatory_fields(self):
        metadata = MetadataEndpoint([], self.metadata)
        self.assertIn("issuer", metadata.claims)
        self.assertEqual(metadata.claims["issuer"], 'https://foo.bar')
