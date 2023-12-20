import dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
from src.blockchain.live_data_fetch import BlockChainDataFetch
from src.blockchain.fetch import BlockChainData
from src.mapper.graph_map import convert_to_threejs_format
from src.threat_actor.app import ThreatActorController
from src.profiling.app import ProfileController
import logging
dotenv.load_dotenv()
print(CORS(app))
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


threat_actor_controller = ThreatActorController()
profile_controller = ProfileController()

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




@app.route('/threat_actors/create', methods=['POST'])
def create_threat_actor_route():
    data = request.get_json()
    if not data:
        return {"error": "request body is required"}
    return threat_actor_controller.create_threat_actor_on_es(data)

@app.route('/threat_actors', methods=['GET'])
def get_all_threat_actors():
    print("search_query")
    param_value = request.args.get('search_query', None)
    if param_value:
        res = threat_actor_controller.search_anything(param_value)
        return res
    else:
        res = threat_actor_controller.search_all()
        return res
    
@app.route('/profile/create', methods=['POST'])
def create_profile_route():
    data = request.get_json()
    if not data:
        return {"error": "request body is required"}
    return profile_controller.create_profile(data)


@app.route('/profile', methods=['GET'])
def get_all_profiles_route():

    uid = request.args.get('uid', None)
    if uid:
        return profile_controller.get_profile(uid)
    else:
        return profile_controller.get_all_profiles()

@app.route('/profile', methods=['DELETE'])
def delete_profile_route():
    data = request.get_json()
    if not data:
        return {"error": "request body is required"}
    return profile_controller.delete_profile(data)


    



# @app.route('/threat_actors/load_scrapped_dataset', methods=['GET'])
# def load_scrapped_dataset_route():
#     load_scrapped_dataset()
#     return {"message": "success"}


   


if __name__ == '__main__':
    app.run(debug=True,port=5115)
