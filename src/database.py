import logging
import os
import uuid
from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy, PartitionKey
from azure.cosmos.exceptions import CosmosHttpResponseError, CosmosResourceNotFoundError
from .config import get_cosmos_config

logger = logging.getLogger(__name__)


def get_cosmos_client():
    """Get Cosmos DB client with proper error handling."""
    try:
        config = get_cosmos_config()
        if not config or not config.validate_config():
            logger.warning("Cosmos DB config not available or invalid")
            return None

        connection_params = config.get_connection_params()

        if "connection_string" in connection_params:
            client = CosmosClient.from_connection_string(
                connection_params["connection_string"],
                connection_verify=config.verify_ssl,
            )
        else:
            client = CosmosClient(
                connection_params["endpoint"],
                connection_params["key"],
                connection_verify=config.verify_ssl,
            )

        return client
    except Exception as e:
        logger.error(f"Failed to create Cosmos DB client: {e}")
        return None


def ensure_database_and_container():
    """Ensure database and container exist, create if they don't."""
    try:
        client = get_cosmos_client()
        if not client:
            logger.warning("Cannot ensure database/container - client not available")
            return None, None

        config = get_cosmos_config()
        if not config:
            logger.warning("Cannot ensure database/container - config not available")
            return None, None

        # Create database if it doesn't exist
        try:
            database = client.create_database_if_not_exists(id=config.database_name)
            logger.info(f"Database '{config.database_name}' ready")
        except Exception as e:
            logger.error(f"Failed to create/get database: {e}")
            return None, None

        # Create container if it doesn't exist
        try:
            container = database.create_container_if_not_exists(
                id=config.container_name,
                partition_key=PartitionKey(path="/id"),
                offer_throughput=400,
            )
            logger.info(f"Container '{config.container_name}' ready")
            return database, container
        except Exception as e:
            logger.error(f"Failed to create/get container: {e}")
            return database, None

    except Exception as e:
        logger.error(f"Failed to ensure database and container: {e}")
        return None, None


def get_container() -> ContainerProxy:
    """Get Cosmos DB container with proper error handling."""
    try:
        database, container = ensure_database_and_container()
        return container
    except Exception as e:
        logger.error(f"Failed to get container: {e}")
        return None


def get_database():
    """Get Cosmos DB database with proper error handling."""
    try:
        database, _ = ensure_database_and_container()
        return database
    except Exception as e:
        logger.error(f"Failed to get database: {e}")
        return None


def save_analysis_result(data: dict, container=None):
    """Save analysis result to Cosmos DB with error handling."""
    try:
        if container is None:
            container = get_container()

        if not container:
            logger.warning("Container not available, skipping save")
            return {"saved": False, "reason": "Container not available"}

        # Ensure the document has an id field for Cosmos DB
        if "id" not in data:
            import uuid

            data["id"] = str(uuid.uuid4())

        result = container.create_item(body=data)
        logger.info(f"Analysis result saved with id: {data['id']}")
        return {"saved": True, "id": data["id"]}

    except CosmosResourceNotFoundError as e:
        logger.error(f"Cosmos DB resource not found: {e}")
        return {"saved": False, "reason": "Resource not found"}
    except Exception as e:
        logger.error(f"Failed to save analysis result: {e}")
        return {"saved": False, "reason": str(e)}
