import os
import logging
import urllib3
from typing import Optional

# Disable SSL warnings for local development
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

# Global variable to hold the config instance
_cosmos_config_instance = None


class CosmosDBConfig:
    def __init__(self):
        try:
            # Connection string takes precedence if provided
            self.connection_string: Optional[str] = os.getenv(
                "COSMOS_DB_CONNECTION_STRING"
            )

            # Fallback to endpoint + key if connection string not provided
            self.endpoint: str = os.getenv(
                "COSMOS_DB_ENDPOINT", "https://localhost:8081"
            )
            self.key: str = os.getenv(
                "COSMOS_DB_KEY",
                "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
            )

            # Database and container configuration
            self.database_name: str = os.getenv(
                "COSMOS_DB_DATABASE_NAME", "data-analyzer"
            )
            self.container_name: str = os.getenv(
                "COSMOS_DB_CONTAINER_NAME", "analysis-results"
            )

            # Connection settings with error handling for invalid values
            self.timeout: int = self._safe_int_env("COSMOS_DB_TIMEOUT", 30)
            self.max_retry_attempts: int = self._safe_int_env(
                "COSMOS_DB_MAX_RETRY_ATTEMPTS", 3
            )
            self.retry_fixed_interval: int = self._safe_int_env(
                "COSMOS_DB_RETRY_FIXED_INTERVAL", 5
            )

            # SSL settings for local development
            self.verify_ssl: bool = (
                os.getenv("COSMOS_DB_VERIFY_SSL", "false").lower() == "true"
            )

            logger.info("Cosmos DB configuration loaded successfully")

        except Exception as e:
            logger.error(f"Error initializing Cosmos DB configuration: {e}")
            # Set safe defaults on error
            self._set_defaults()

    def _safe_int_env(self, env_var: str, default: int) -> int:
        """Safely convert environment variable to int with fallback."""
        try:
            return int(os.getenv(env_var, str(default)))
        except (ValueError, TypeError):
            logger.warning(f"Invalid value for {env_var}, using default: {default}")
            return default

    def _set_defaults(self):
        """Set safe default values in case of initialization error."""
        self.connection_string = None
        self.endpoint = "https://localhost:8081"
        self.key = "C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=="
        self.database_name = "data-analyzer"
        self.container_name = "analysis-results"
        self.timeout = 30
        self.max_retry_attempts = 3
        self.retry_fixed_interval = 5
        self.verify_ssl = False

    def get_connection_params(self) -> dict:
        """Return connection parameters, prioritizing connection string if available."""
        try:
            if self.connection_string:
                return {"connection_string": self.connection_string}
            else:
                return {"endpoint": self.endpoint, "key": self.key}
        except Exception as e:
            logger.error(f"Error getting connection parameters: {e}")
            return {"endpoint": "https://localhost:8081", "key": self.key}

    def validate_config(self) -> bool:
        """Validate the configuration is usable."""
        try:
            if self.connection_string:
                return bool(self.connection_string.strip())
            return bool(self.endpoint and self.key)
        except:
            return False


def get_cosmos_config() -> Optional[CosmosDBConfig]:
    """Get cosmos config instance with lazy loading and error handling."""
    global _cosmos_config_instance

    if _cosmos_config_instance is None:
        try:
            _cosmos_config_instance = CosmosDBConfig()
        except Exception as e:
            logger.error(f"Failed to initialize cosmos config: {e}")
            return None

    return _cosmos_config_instance


# For backward compatibility, but now safely handled
try:
    cosmos_config = get_cosmos_config()
except Exception as e:
    logger.error(f"Failed to initialize cosmos_config: {e}")
    cosmos_config = None
