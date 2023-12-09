import requests
import json
import os
import logging

class BlockChainDataFetch():
    def __init__(self):
        self.base_url = "https://blockchain.info"
        self.block_tx_url = "/rawtx/"
        self.block_address_url = "/rawaddr/"
        self.cache_dir = os.path.join(os.path.dirname(__name__), 'cache')
        self.current_cache = {"transaction": {}, "address": {}}
        self.local_init_cache("transaction")
        self.local_init_cache("address")

    def local_update_cache(self, cache_type, object_key, data):
        self.current_cache[cache_type][object_key] = data
        cache_file = os.path.join(self.cache_dir, cache_type + '.json')
        with open(cache_file, 'w') as f:
            json.dump(self.current_cache[cache_type], f)

    def local_init_cache(self, cache_type):
        cache_file = os.path.join(self.cache_dir, cache_type + '.json')
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                data = json.load(f)
            self.current_cache[cache_type] = data

    def local_find_cache(self, cache_type, key):
        return self.current_cache[cache_type].get(key, None)

    def blockchain_transaction_data(self, tx_hash):
        url = self.base_url + self.block_tx_url + tx_hash
        response = requests.get(url)
        return response.json()

    def blockchain_address_data(self, address):
        url = self.base_url + self.block_address_url + address
        response = requests.get(url)
        return response.json()

    def get_transaction_data(self, tx_hash):
        cache = self.local_find_cache("transaction", tx_hash)
        if cache:
            logging.info("Using Cache for Transaction: " + tx_hash)
            return cache
        else:
            logging.info("Fetching Transaction Live: " + tx_hash)
            data = self.blockchain_transaction_data(tx_hash)
            self.local_update_cache("transaction", tx_hash, data)
            return data

    def get_address_data(self, address):
        cache = self.local_find_cache("address", address)
        if cache:
            logging.info("Using Cache for Address: " + address)
            return cache
        else:
            logging.info("Fetching Address Live: " + address)
            data = self.blockchain_address_data(address)
            self.local_update_cache("address", address, data)
            return data
