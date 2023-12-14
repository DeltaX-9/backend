from src.db.mongodb import MongoDB
import os
import requests
import logging

class BlockChainData():
    def __init__(self):
        self.cache_db = MongoDB(os.getenv("CACHE_DB"), "cache")
        self.base_url = "https://api.blockchair.com"
        self.transaction_url = "/{}/dashboards/transaction/{}"
        self.address_url = "/{}/dashboards/address/{}?transaction_details=true"

    def get_database_connection_status(self):
        return self.cache_db.connection_status()

    def get_transaction_data(self, tx_hash, btc_chain):
        cache = self.cache_db.find_one({"key": f"{btc_chain}_transaction_{tx_hash}"})
        if cache:
            logging.info(f"Using Cache for Transaction: {tx_hash}")
            return cache["data"]
        else:
            logging.info(f"Fetching Transaction: {tx_hash}")
            url = self.base_url + self.transaction_url.format(btc_chain, tx_hash)
            response = requests.get(url)
            data = response.json()

            ## BlockChair Structure
            data = data['data'][tx_hash]

            self.cache_db.insert({"key": f"{btc_chain}_transaction_{tx_hash}", "data": data})
            return data
        
    def get_address_data(self, address, btc_chain):
        cache = self.cache_db.find_one({"key": f"{btc_chain}_address_{address}"})
        if cache:
            logging.info(f"Using Cache for Address: {address}")
            return cache["data"]
        else:
            logging.info(f"Fetching Address: {address}")
            url = self.base_url + self.address_url.format(btc_chain, address)
            response = requests.get(url)
            data = response.json()

            ## BlockChair Structure
            data = data['data'][address]

            self.cache_db.insert({"key": f"{btc_chain}_address_{address}", "data": data})
            return data
        
    