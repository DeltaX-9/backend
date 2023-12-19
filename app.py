import dotenv
from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from src.blockchain.live_data_fetch import BlockChainDataFetch
from src.blockchain.fetch import BlockChainData
from src.mapper.graph_map import convert_to_threejs_format
from src.threat_actor.app import find_threat_actor_by_id, create_threat_actor, find_by_address, find_all_threat_actors
from src.automation.app import load_scrapped_dataset
import logging
dotenv.load_dotenv()
print(CORS(app))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



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


@app.route('/threat_actors/find', methods=['POST'])
def find_threat_actor():
    data = request.get_json()
    if not data:
        return {"error": "request body is required"}
    if not data.get("id"):
        return {"error": "id is required"}
    res = find_threat_actor_by_id(data.get("id"))
    return res

@app.route('/threat_actors/create', methods=['POST'])
def create_threat_actor():
    data = request.get_json()
    if not data:
        return {"error": "request body is required"}
    # if not data.get("type") or not data.get("chain") or not data.get("address") or not data.get("threat_level") or not data.get("threat_score"):
        # return {"error": "type, chain, address, threat_level, threat_score are required"}
    res = create_threat_actor(data)
    return res

@app.route('/threat_actors/find_by_address', methods=['POST'])
def find_threat_actor_by_address():
    data = request.get_json()
    if not data:
        return {"error": "request body is required"}
    if not data.get("address"):
        return {"error": "address is required"}
    res = find_by_address(data.get("address"), "threat_actors")
    return res

@app.route('/threat_actors/load_scrapped_dataset', methods=['GET'])
def load_scrapped_dataset_route():
    load_scrapped_dataset()
    return {"message": "success"}

@app.route('/threat_actors', methods=['GET'])
def get_all_threat_actors():
    res = find_all_threat_actors()
    return res
   


if __name__ == '__main__':
    app.run(debug=True,port=5115)
