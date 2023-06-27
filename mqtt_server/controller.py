# controller.py - class to talk to the database

from pymongo import MongoClient
from scan import Scan

class Controller:
    def __init__(self, cluster_uri: str) -> None:
        """Controller constructor

        Args:
            cluster_uri (str): URI to MongoDB Cluster
        """
        self.cluster = MongoClient(cluster_uri)
        self.database = None
        self.collection = None

    def switch_database(self, database: str) -> None:
        """Switch database

        Args:
            database (str): Database name
        """
        self.database = self.cluster[database]
    
    def switch_collection(self, collection: str) -> None:
        """Switch collection

        Args:
            collection (str): Collection name
        """
        if self.database is not None:
            self.collection = self.database[collection]
    
    def check_database(self, database: str) -> bool:
        """Check if a database exists

        Args:
            database (str): Database name

        Returns:
            bool: Returns True if database exists, else False
        """
        if database in self.cluster.list_database_names():
            return True
        else:
            return False
    
    def check_collection(self, collection: str) -> bool:
        """Check if a collection exists

        Args:
            collection (str): Collection name

        Returns:
            bool: Returns True if collection exists, else False
        """
        if self.database is not None and collection in self.database.list_collection_names():
            return True
        else:
            return False

    def add_scan(self, scan: Scan) -> None:
        """Add a list of product objects to the active collection

        Args:
            products (list): List of product objects
        """
        self.collection.insert_one(scan.to_dict())

    def get_products(self) -> list:
        if self.collection is not None:
            scans = self.collection.find({})
            return list(scans)
        else:
            return []

    def get_last_id(self) -> int:
        scans = self.get_products()
        if len(scans) > 0: 
            return scans[-1][0]
        else:
            return -1