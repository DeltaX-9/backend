from elasticsearch import Elasticsearch
import json
import os

es = Elasticsearch("http://localhost:9200")
index_name = "threat_actors"
index_file_path = f"./mapping/{index_name}.json"
print(index_file_path)
mapping_data = json.load(open(index_file_path, "r"))   


es.indices.create(index=index_name, body=mapping_data, ignore=400)



# sample_data = {'id': 'address_bitcoin_bc1qp6k6tux6g3gr3sxw94g9tx4l0cjtu2pt65r6xp', 'wallet': {'address': 'bc1qp6k6tux6g3gr3sxw94g9tx4l0cjtu2pt65r6xp', 'chain': 'bitcoin', 'forensics': {'threat_level': 'high', 'threat_score': 90}}}



# def insert_data(data):
#     es.index(index=index_name, body=data)

# def search_data(query):
#     res = es.search(index=index_name, body=query)
#     return res

# insert_data(sample_data)
# # res = search_data({
# #     "query": {
# #         "match": {
# #             "source_url": "http://example.com"
# #         }
# #     }
# # })

# # print(res)

# # print(es.info())



