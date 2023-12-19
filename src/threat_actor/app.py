from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

import json
from flask import Flask, jsonify

es = Elasticsearch("http://localhost:9200")

def insert_data_into_es(index_name,data):
    return es.index(index=index_name, body=data)

def create_threat_actor(threat_actor):
    index_name = "threat_actors"
    
    type = threat_actor["type"]

    if type == "address":
        data = {
            "id": f"{threat_actor['type']}_{threat_actor['address']}",
            "wallet":{
                "address": threat_actor["address"],
                "chain": threat_actor["chain"],
                "summary": threat_actor["summary"],
                "records": threat_actor["records"],
                "target_url": threat_actor["target_url"],
                "transaction_id": threat_actor["transaction_id"],
                "threat_level": threat_actor["threat_level"],
                "threat_score": threat_actor["threat_score"],
            }
        }
        res = insert_data_into_es(index_name, data)

        # Check if the indexing was successful
        if res["result"] == "created":
            return jsonify({"message": "Threat actor created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create threat actor"}), 500

    elif type == "user":
        data = {
            "id": f"{threat_actor['type']}_{threat_actor['user_identification']}",
            "user":{
                "source_url": threat_actor["source_url"],
                "user_identification": threat_actor["user_identification"],
                "summary": threat_actor["summary"],
                "records": threat_actor["records"],
                "forensics": {
                    "threat_level": threat_actor["threat_level"],
                    "threat_score": threat_actor["threat_score"],
                }
            }
        }
        res = insert_data_into_es(index_name, data)

        # Check if the indexing was successful
        if res["result"] == "created":
            return jsonify({"message": "Threat actor created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create threat actor"}), 500

    else:
        return jsonify({"error": "Invalid threat actor type"}), 400

def find_by_address(address, index_name):
    index_name = "threat_actors"
    search_query = Search(using=es, index=index_name).query(
        Q("match", wallet__address=address)
    )

    response = search_query.execute()
    results_list = [hit.to_dict() for hit in response]

    # Return the results as a Flask response
    return jsonify({"results": results_list})

def find_all_threat_actors():
    index_name = "threat_actors"
    search_query = Search(using=es, index=index_name).query(
        Q("match_all")
    )

    response = search_query.execute()
    results_list = [hit.to_dict() for hit in response]

    # Return the results as a Flask response
    return jsonify({"results": results_list})

def find_threat_actor_by_id(id):
    index_name = "threat_actors"
    res = es.search(index=index_name, body={
        "query": {
            "match": {
                "id": id
            }
        }
    })
    return res