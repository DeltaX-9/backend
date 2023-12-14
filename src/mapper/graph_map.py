def convert_to_threejs_format(data):
    # Extract relevant information from the JSON data
    tx_hash = data["hash"]
    inputs = data["inputs"]
    outputs = data["out"]


    # Create wallet nodes for inputs
    wallet_nodes_inputs = [
        {"id": input["prev_out"]["addr"], "type": "wallet"} for input in inputs
    ]

    # Create wallet nodes for outputs
    wallet_nodes_outputs = [
        {"id": output["addr"], "type": "wallet"} for output in outputs
    ]

    # Create transaction node
    transaction_node = {"id": tx_hash, "type": "transaction"}

    # Combine all nodes
    nodes = wallet_nodes_inputs + wallet_nodes_outputs + [transaction_node]

    # Create links for inputs
    links_inputs = [
        {"source": input["prev_out"]["addr"], "target": tx_hash} for input in inputs
    ]

    # Create links for outputs
    links_outputs = [
        {"source": tx_hash, "target": output["addr"]} for output in outputs
    ]

    # Combine all links
    links = links_inputs + links_outputs

    # Combine nodes and links into a dictionary
    result = {"nodes": nodes, "links": links}

    return result




# # Example usage
# input_data = {
#     "hash": "b6f6991d03df0e2e04dafffcd6bc418aac66049e2cd74b80f14ac86db1e3f0da",
#     "ver": 1,
#     "vin_sz": 1,
#     "vout_sz": 2,
#     "lock_time": "Unavailable",
#     "size": 258,
#     "relayed_by": "64.179.201.80",
#     "block_height": 12200,
#     "tx_index": "12563028",
#     "inputs": [
#         {
#             "prev_out": {
#                 "hash": "a3e2bcc9a5f776112497a32b05f4b9e5b2405ed9",
#                 "value": "100000000",
#                 "tx_index": "12554260",
#                 "n": "2",
#             },
#             "script": "76a914641ad5051edd97029a003fe9efb29359fcee409d88ac",
#         }
#     ],
#     "out": [
#         {
#             "value": "98000000",
#             "hash": "29d6a3540acfa0a950bef2bfdc75cd51c24390fd",
#             "script": "76a914641ad5051edd97029a003fe9efb29359fcee409d88ac",
#         },
#         {
#             "value": "2000000",
#             "hash": "17b5038a413f5c5ee288caa64cfab35a0c01914e",
#             "script": "76a914641ad5051edd97029a003fe9efb29359fcee409d88ac",
#         },
#     ],
# }

# result = convert_to_threejs_format(input_data)
# print(result)
