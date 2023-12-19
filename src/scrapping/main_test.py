from extractor import DataExtractor
import os


for x in range(1,3):
    print("Test case: ", x)
    
    # Test case 1: Test the extractor with a local file

    html_file = os.path.join(os.path.dirname(__file__), f'./dataset/darkweb_{x}.html')
    extractor = DataExtractor(html_file, TESTING=True)

    print("Title: ", extractor.title)
    print("Bitcoin addresses: ", extractor.bitcoin_addresses)
    print("IP addresses: ", extractor.ip_addresses)
    print("Links: ", extractor.links)
    print("Images: ", extractor.images)
    print("Meta: ", extractor.meta)
    # print("Text: ", extractor.text)
    print("------------------------------------------------------")





