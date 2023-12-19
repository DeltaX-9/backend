from src.threat_actor.app import create_threat_actor
from src.scrapping.extractor import DataExtractor
import json
import os


def load_scrapped_dataset():
    for x in range(1,3):
        html_file_path = os.path.join(os.path.dirname(__file__), f"../dataset/darkweb_{x}.html")
        extracted_html = DataExtractor(html_file_path, TESTING=True)
        
        for address in extracted_html.bitcoin_addresses:
            create_threat_actor({
                "type": "address",
                "chain": "bitcoin",
                "address": address,
                "threat_level": "unknown",
                "threat_score": 0,
                "target_url": "http://nzdnmfcf2z5pd3vwfyfy3jhwoubv6qnumdglspqhurqnuvr52khatdad.onion", ## This can be changed to the actual url
                "transaction_id": "",
                "summary": "",
                "records": []
            })









