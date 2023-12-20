from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, query
from elasticsearch_dsl import Search, Q

import json
from flask import Flask, jsonify

es = Elasticsearch("http://localhost:9200")


class ThreatActorController:
    def __init__(self):
        self.index_name = "threat_actors"

    def insert_data_into_es(self, index_name, data, id):
        return es.update(index=index_name, id=id, body={"doc": data, "doc_as_upsert": True})

    def create_threat_actor_on_es(self, data):
        try:
            threat_actor_id = data["id"]

            # Check if the threat actor already exists
            existing_threat_actor = es.get(index=self.index_name, id=threat_actor_id, ignore=404)

            if existing_threat_actor and existing_threat_actor["found"]:
                # Threat actor exists, append the new activity
                existing_activities = existing_threat_actor["_source"].get("activities", [])
                new_activity = data.get("activities", [])

                # Append the new activity to the existing activities
                existing_activities.extend(new_activity)

                # Update the existing document with the new activities
                update_body = {
                    "script": {
                        "source": "ctx._source.activities = params.activities",
                        "lang": "painless",
                        "params": {"activities": existing_activities}
                    }
                }

                # Perform the update by query
                es.update_by_query(index=self.index_name, body={
                    "query": {"term": {"id": threat_actor_id}},
                    "script": update_body["script"]
                })

                return jsonify({"message": "Threat actor updated successfully"}), 200
            else:
                # Threat actor does not exist, create a new one
                res = self.insert_data_into_es(self.index_name, data, threat_actor_id)
                if res["result"] == "updated" or res["result"] == "created":
                    return jsonify({"message": "Threat actor created successfully"}), 201
                else:
                    return jsonify({"error": "Failed to create threat actor"}), 500

        except Exception as e:
            return jsonify({"error": f"Failed to create/update threat actor: {str(e)}"}), 500
        
    def search_all(self):
        try:
            # Create a Search object without specifying a query, which matches all documents
            s = Search(using=es, index=self.index_name)

            # Execute the search
            result = s.execute()

            documents_list = []
            for hit in result.hits:
                # Convert the entire hit (document) to a dictionary
                document_dict = hit.to_dict()

                # Optionally, you may want to include the nested activities field separately
                if "activities" in document_dict:
                    document_dict["activities"] = [activity.to_dict() for activity in hit.activities]

                documents_list.append(document_dict)

            # Return the list of documents as JSON
            return jsonify({"documents": documents_list})
                    
                    
            
        except Exception as e:  
            return {"error": str(e)}

    def search_anything(self,search_query):
        try:
            query = Q("nested", path="activities", query=Q("match", activities__content=search_query))

            s = Search(using=es, index=self.index_name).query(query)
            result = s.execute()

            documents_list = []
            for hit in result.hits:
                # Convert the entire hit (document) to a dictionary
                document_dict = hit.to_dict()

                # Optionally, you may want to include the nested activities field separately
                document_dict["activities"] = [activity.to_dict() for activity in hit.activities]

                documents_list.append(document_dict)

            # Return the list of documents as JSON
            return jsonify({"documents": documents_list})
            
                    
            
        except Exception as e:  
            return {"error": str(e)}