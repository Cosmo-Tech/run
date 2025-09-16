"""Utility functions for managing Keycloak tokens."""

import logging
import time

from keycloak import KeycloakOpenID

logger = logging.getLogger(__name__)


class Authenticate:
    """Manages Keycloak token retrieval and refresh."""

    def __init__(
        self, server_url: str, realm_name: str, client_id: str, client_secret: str
    ):
        """Initialize the Keycloak token manager."""
        self.keycloak_openid = KeycloakOpenID(
            server_url=server_url,
            client_id=client_id,
            realm_name=realm_name,
            client_secret_key=client_secret,
        )
        self.access_token = None
        self.token_expiry = None

    def refresh_token(self) -> str:
        """Refresh the access token."""
        try:
            token = self.keycloak_openid.token(grant_type="client_credentials")
            self.access_token = token["access_token"]
            self.token_expiry = time.time() + token["expires_in"]
            logger.info("Token refreshed successfully")
            return self.access_token
        except Exception as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            raise RuntimeError(f"Failed to refresh token: {e}")

    def get_token(self) -> str:
        """Get the current access token, refreshing it if necessary."""
        if self.access_token is None or time.time() >= self.token_expiry:
            return self.refresh_token()
        return self.access_token
