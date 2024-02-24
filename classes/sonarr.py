from pyarr import SonarrAPI
from classes.download_client import DownloadClient


class Sonarr:
    def __init__(self, api, host, download_clients):
        self.api = api
        self.host = host
        self.client = SonarrAPI(self.host, self.api)
        self.download_clients = []
        self.indexers = self.get_indexers()
        self.get_download_clients(download_clients)
    
    def get_indexers(self):
        return self.client.get_indexer()
    
    def get_download_clients(self, download_clients):
        for i in self.client.get_download_client():
            additional_fields = { 
                "enabled" : i["enable"], 
                "hostname" : i["fields"][0]["value"], 
                "port" : i["fields"][1]["value"], 
                "privacy" : [d.privacy for d in download_clients if d.name==i["name"]][0],
            }
            self.download_clients.append(DownloadClient(i|additional_fields))
    
    def get_download_client_id(self, download_client):
        print(download_client)
        breakpoint()
        return download_client.id