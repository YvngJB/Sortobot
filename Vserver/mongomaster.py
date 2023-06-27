# controller.py - class to talk to the database

from queue import Empty
from pymongo import MongoClient
from scan import Scan
class MongoMaster:
    # cluster_uri (str): URI to MongoDB Cluster
    def __init__(self, cluster_uri: str) -> None:
        self.cluster = MongoClient(cluster_uri)
        self.database = None
        self.collection = None

    def switch_dbase(self, database: str) -> None:
    # database (str): Database name
        self.database = self.cluster[database]
    
    def switch_collection(self, collection: str) -> None:
        #Switch collection collection (str): Collection name
        if self.database is not None:
            self.collection = self.database[collection]
    
    def check_dbase(self, database: str) -> bool:
        #Check if a database exists database (str): Database name
        if database in self.cluster.list_database_names():
            return True
        else:
            return False
    
    def check_collection(self, collection: str) -> bool:
        # Check if a collection exists
        # bool: Returns True if collection exists, else False
        if self.database is not None and collection in self.database.list_collection_names():
            return True
        else:
            return False

    def add_scan(self, scan: Scan) -> None:
        #Add a list of product objects to the active collection
        self.collection.insert_one(scan.to_dict())

    def get_products(self) -> list:
        if self.collection is not None:
            scans = self.collection.find({})
            return list(scans)
        else:
            return []

    def get_next_id(self) -> int:
        if len(self.get_products()) > 0: 
            return self.collection.find().sort([('timestamp', -1)]).limit(1)[0]["_id"] + 1
        else:
            return 0
