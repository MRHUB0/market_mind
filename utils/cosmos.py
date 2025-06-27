# utils/cosmos.py
import os
from azure.cosmos import CosmosClient

# Load environment variables
COSMOS_DB_URI = os.getenv("COSMOS_DB_URI")
COSMOS_DB_PRIMARY_KEY = os.getenv("COSMOS_DB_PRIMARY_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME")

# Initialize Cosmos client
client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_PRIMARY_KEY)

def get_container(container_name):
    """
    Retrieve a Cosmos DB container client by name.
    """
    database = client.get_database_client(COSMOS_DB_NAME)
    return database.get_container_client(container_name)
