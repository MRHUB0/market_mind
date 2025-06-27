# utils/cosmos.py
import os
from azure.cosmos import CosmosClient

COSMOS_DB_URI = os.getenv("COSMOS_DB_URI")
COSMOS_DB_PRIMARY_KEY = os.getenv("COSMOS_DB_PRIMARY_KEY")
COSMOS_DB_NAME = os.getenv("COSMOS_DB_NAME")
COSMOS_DB_CONTAINER = os.getenv("COSMOS_DB_CONTAINER")

client = CosmosClient(COSMOS_DB_URI, credential=COSMOS_DB_PRIMARY_KEY)
database = client.get_database_client(COSMOS_DB_NAME)
container = database.get_container_client(COSMOS_DB_CONTAINER)
