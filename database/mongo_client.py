"""
Database connection module.
"""
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from database.config import config


class Db:
    """
    Establishes a Db instance.
    """

    def __init__(self):
        self.uri = config.MONGO_CONNECTION_URL
        if not self.uri:
            raise ValueError("Db connection URL is not defined")

        self.client = MongoClient(self.uri, server_api=ServerApi("1"))

        try:
            self.client.admin.command("ping")
            print("Pinged your deployment. Successfully connected to MongoDB.")
        except Exception as error:
            print(f"MongoDB connection error: {error}")
            raise

        self.db = self.client["mm_DB1"]

    def insert_one_document(self, collection_name, data):
        """
        Insert one document in an specific db collection
        """
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            print(e)

if __name__ == "__main__":
    print("Iniciando o teste de inserção no Atlas...")

    db = Db()
    data = {
        "sku": "GTR-PRO-001",
        "name": "Fender Stratocaster Profissional",
        "price": 1500.00,
        "color": "Sunburst",
        "strings": 6,
    }

    try:
        novo_id = db.insert_one_document("product", data)
        print(f"✅ SUCESSO TOTAL! A guitarra foi salva no Atlas com o ID: {novo_id}")
    except Exception as e:
        print(e)