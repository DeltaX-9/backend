# app.py
from flask import Flask
from src.blockchain.live_data_fetch import BlockChainDataFetch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/blockchain/transaction/<tx_hash>')
def get_transaction_data(tx_hash):
    return BlockChainDataFetch().get_transaction_data(tx_hash)

if __name__ == '__main__':
    app.run(debug=True)
