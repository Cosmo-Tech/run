"""Configuration management for the brewery automation script."""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from run.authenticate import Authenticate

# Load environment variables from .env file
load_dotenv()


@dataclass
class Config:
    """Configuration settings for the automation script."""

    api_url: str
    access_token: str
    organization_id: Optional[str]
    log_level: str
    template_dir: Path

    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables."""
        required_vars = {
            "COSMOTECH_API_URL": "API URL",
            "SERVER_URL": "Keycloak Server URL",
            "REALM_NAME": "Keycloak Realm Name",
            "COSMOTECH_CLIENT_ID": "Client ID",
            "COSMOTECH_CLIENT_SECRET": "Client Secret",
        }

        # Check required variables
        missing = [var for var, name in required_vars.items() if not os.getenv(var)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        # Get optional variables with defaults
        organization_id = os.getenv("ORGANIZATION_ID")
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        # Validate log level
        if log_level not in logging._nameToLevel:
            raise ValueError(f"Invalid log level: {log_level}")

        # Set template directory relative to project root
        project_root = Path(__file__).parent.parent
        template_dir = project_root / "templates"

        # Initialize Authenticator
        token_manager = Authenticate(
            server_url=os.getenv("SERVER_URL"),
            realm_name=os.getenv("REALM_NAME"),
            client_id=os.getenv("COSMOTECH_CLIENT_ID"),
            client_secret=os.getenv("COSMOTECH_CLIENT_SECRET"),
        )

        return cls(
            api_url=os.getenv("COSMOTECH_API_URL"),
            access_token=token_manager.get_token(),
            organization_id=organization_id,
            log_level=log_level,
            template_dir=template_dir,
        )

    def validate_template_dir(self) -> None:
        """Ensure template directory exists and contains required files."""
        if not self.template_dir.exists():
            raise FileNotFoundError(
                f"Template directory not found: {self.template_dir}"
            )

        required_templates = [
            "Organization.yaml",
            "Solution.yaml",
            "Runner.yaml",
            "Workspace-dev.yaml",
        ]

        missing = []
        for template in required_templates:
            if not (self.template_dir / template).exists():
                missing.append(template)

        if missing:
            raise FileNotFoundError(
                f"Missing required template files: {', '.join(missing)}"
            )
