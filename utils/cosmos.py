import os
from azure.cosmos import CosmosClient, PartitionKey

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DB_NAME = "marketmind"

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
db = client.create_database_if_not_exists(COSMOS_DB_NAME)

def get_container(name):
    return db.create_container_if_not_exists(
        id=name,
        partition_key=PartitionKey(path="/userId"),
        offer_throughput=400
    )
