from src.db.mongodb import MongoDB
import os
import requests
import logging
from flask import jsonify
import random
import string


class ProfileController:
    def __init__(self) -> None:
        self.cache_db = MongoDB(os.getenv("CACHE_DB"), "profile")
        
    def get_database_connection_status(self):
        return self.cache_db.connection_status()
    
    def get_profile(self, profile_id):
        try:
            profile = self.cache_db.find_one({"uid": f"{profile_id}"})
            if profile:
                profile.pop('_id')
                return jsonify(profile), 200
            else:
                return jsonify({"message": "Profile does not exist"}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to fetch profile: {str(e)}"}), 500
    

    def get_all_profiles(self):
        try:
            profiles = self.cache_db.find({})
            data = []
            for x in profiles:
                x.pop('_id')
                data.append(x)

            return jsonify(data), 200
        except Exception as e:
            return jsonify({"error": f"Failed to fetch profiles: {str(e)}"}), 500
    
    def create_profile(self,data):
        try:
            print(data)
            print(self.get_database_connection_status())
            print(''.join(random.choices(string.ascii_lowercase, k=10)))
            profile_id = data["uid"]
            existing_profile = self.cache_db.find_one({"uid": f"{profile_id}"})
            if existing_profile:
                return jsonify({"message": "Profile already exists"}), 409
            else:
                self.cache_db.insert({
                    "uid": ''.join(random.choices(string.ascii_lowercase, k=10)),
                    "name": data["name"],
                    "description": data["description"],
                    "is_active": data["is_active"],
                    "threat_actor": data["threat_actor"],
                    "references": data["references"],
                    "tags": data["tags"],
                    "aliases": data["aliases"],
                })
                return jsonify({"message": "Profile created successfully"}), 201
        except Exception as e:
            print(e)
            return jsonify({"error": f"Failed to create profile: {str(e)}"}), 500
        
    def update_profile(self, data):
        try:
            profile_id = data["id"]
            existing_profile = self.cache_db.find_one({"id": f"{profile_id}"})
            
            if existing_profile:
                update_fields = {}

                # Update only the fields that are provided by the client
                if "name" in data:
                    update_fields["name"] = data["name"]
                if "description" in data:
                    update_fields["description"] = data["description"]
                if "is_active" in data:
                    update_fields["is_active"] = data["is_active"]
                if "threat_actor" in data:
                    update_fields["threat_actor"] = data["threat_actor"]
                if "references" in data:
                    update_fields["references"] = data["references"]
                if "tags" in data:
                    update_fields["tags"] = data["tags"]
                if "aliases" in data:
                    update_fields["aliases"] = data["aliases"]

                self.cache_db.update({"id": profile_id}, update_fields)

                return jsonify({"message": "Profile updated successfully"}), 200
            else:
                return jsonify({"message": "Profile does not exist"}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to update profile: {str(e)}"}), 500

    def delete_profile(self, profile_id):
        try:
            existing_profile = self.cache_db.find_one({"id": f"{profile_id}"})
            if existing_profile:
                self.cache_db.delete({"uid": profile_id})
                return jsonify({"message": "Profile deleted successfully"}), 200
            else:
                return jsonify({"message": "Profile does not exist"}), 404
        except Exception as e:
            return jsonify({"error": f"Failed to delete profile: {str(e)}"}), 500