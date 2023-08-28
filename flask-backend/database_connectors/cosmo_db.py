from azure.cosmos import CosmosClient
import os

class CosmosDBConnection:
    def __init__(self):
        self.client = None
        self.database = None
        self.container = None
        self.connect()

    def connect(self):
        endpoint = os.getenv('COSMOS_DB_ENDPOINT')
        key = os.getenv('COSMOS_DB_KEY')
        database_name = os.getenv('COSMOS_DB_DATABASE_NAME')
        container_name = os.getenv('COSMOS_DB_CONTAINER_NAME')

        try:
            self.client = CosmosClient(endpoint, key)
            self.database = self.client.get_database_client(database_name)
            self.container = self.database.get_container_client(container_name)
            print("Connected to Cosmos DB.")

        except Exception as e:
            print("Error connecting to Cosmos DB:", e)
            self.client = None
            self.database = None
            self.container = None

    def execute_query(self, query):
        if self.container is None:
            self.connect()

        if self.container is not None:
            try:
                items = list(self.container.query_items(
                    query=query,
                    enable_cross_partition_query=True
                ))
                return items

            except Exception as e:
                print("An error occurred executing the query.", e)
                self.container = None
                self.connect()

# Usage
# db = CosmosDBConnection()
# results = db.execute_query("SELECT * FROM c WHERE c.someField = 'someValue'")
