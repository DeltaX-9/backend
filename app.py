import dotenv
from flask import Flask, request
from src.blockchain.live_data_fetch import BlockChainDataFetch
from src.blockchain.fetch import BlockChainData
from src.mapper.graph_map import convert_to_threejs_format
import logging
dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app = Flask(__name__)


blockchain_data = BlockChainData()
if not blockchain_data.get_database_connection_status():
    logging.error("Cache Database Connection Failed")
    exit(1)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/blockchain/transaction/<tx_hash>', methods=['GET'])
def get_transaction_data(tx_hash):
    param_value = request.args.get('btc_chain', None)
    if param_value:
        return blockchain_data.get_transaction_data(tx_hash, param_value)
    else:
        return {"error": "btc_chain parameter is required"}
        

@app.route('/blockchain/address/<address>', methods=['GET'])
def get_address_data(address):
    param_value = request.args.get('btc_chain', None)
    if param_value:
        return blockchain_data.get_address_data(address, param_value)
    else:
        return {"error": "btc_chain parameter is required"}
    
    
@app.route('/blockchain/transaction/<tx_hash>/graph', methods=['GET'])
def get_transaction_graph(tx_hash):
    data =  BlockChainDataFetch().get_transaction_data(tx_hash)
    return convert_to_threejs_format(data)



if __name__ == '__main__':
    app.run(debug=True,port=5115)
