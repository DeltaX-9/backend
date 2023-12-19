import re
from bs4 import BeautifulSoup
from html2text import HTML2Text


class DataExtractor:
    def __init__(self, uri, TESTING=False):
        self.TESTING = TESTING
        self.content = self.get_soup(uri)
        self.bitcoin_addresses = self.extract_bitcoin_address()
        self.text = self.get_text()
        self.title = self.get_title()
        self.links = self.get_links()
        self.images = self.get_images()
        self.meta = self.get_meta()
        self.ip_addresses = self.extract_ip_address()

    def get_soup(self,uri):
        if self.TESTING:
            return BeautifulSoup(open(uri, "r"), 'html.parser')
        else:
            return BeautifulSoup(uri, 'html.parser')
        
    def get_text(self):
        return self.content.get_text()
    
    def get_title(self):
        return self.content.title.string
    
    def get_links(self):
        links = []
        for link in self.content.find_all('a'):
            links.append(link.get('href'))
        return links
    
    def get_images(self):
        images = []
        for image in self.content.find_all('img'):
            images.append(image.get('src'))
        return images
    
    def get_meta(self):
        metas = []
        for meta in self.content.find_all('meta'):
            metas.append(meta.get('content'))
        return metas
    

    #Find all the addresses in the content
    def extract_bitcoin_address(self):
        addresses_set = set()
        # print(self.content)
        for line in str(self.content).splitlines():
            addresses_set.update(re.findall(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}', line))
        return list(addresses_set)
    
    # Find all the IP addresses in the content
    def extract_ip_address(self):
        ip_addresses_set = set()
        for line in str(self.content).splitlines():
            ip_addresses_set.update(re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line))
        return list(ip_addresses_set)



