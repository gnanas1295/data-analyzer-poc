import os
import uuid
from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.container import ContainerProxy

def get_container() -> ContainerProxy:
    ENDPOINT = os.environ.get("COSMOS_DB_ENDPOINT")
    KEY = os.environ.get("COSMOS_DB_KEY")
    DATABASE_NAME = "SimulationDb"
    CONTAINER_NAME = "AnalysisResults"

    client = CosmosClient(ENDPOINT, KEY)
    database = client.create_database_if_not_exists(id=DATABASE_NAME)
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path="/trainee_id"),
    )
    return container

def save_analysis_result(data: dict, container: ContainerProxy) -> dict:
    data["id"] = str(uuid.uuid4())
    container.create_item(body=data)
    return data