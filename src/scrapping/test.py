from extractor import DataExtractor
import os
test_file_path = os.path.join(os.path.dirname(__file__), '../dataset/darkweb_2.html')
scrapped_data = DataExtractor(test_file_path, TESTING=True)

print("BitCoin Address: ",scrapped_data.bitcoin_addresses)
# print(scrapped_data.text)
print("IP Address: ", scrapped_data.ip_addresses)
print("Title: ", scrapped_data.title)
print("Links: ", scrapped_data.links)