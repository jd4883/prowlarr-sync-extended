from pyarr import ReadarrAPI
from classes.download_client import DownloadClient
import json
import requests


class Readarr:
    def __init__(self, api, host, download_clients):
        self.api = api
        self.host = host
        self.client = ReadarrAPI(self.host, self.api)
        self.download_clients = self.get_download_clients()
        self.indexers = self.get_indexers()
        
    
    def get_indexers(self):
        return self.client.get_indexer()
    
    def get_download_clients(self):
        return self.client.get_download_client()

    def get_download_client_id(self):
        return download_client.id

    def parse_indexer_discrepancies(self, indexer, download_client_mappings):
        for ReadarrIndexer in self.indexers:
            if indexer.name == ReadarrIndexer["name"].replace(" (Prowlarr)", ""):
                for k, v in download_client_mappings.items():
                    if (indexer.download_client_id==0):
                        #print(f"ID of {indexer.download_client_id} in prowlarr, no action needed")
                        continue
                    if (indexer.download_client_id == v["prowlarr"]["id"]) and not (v["readarr"]["id"]==ReadarrIndexer["downloadClientId"]):
                        print(f"Parsing Prowlarr Indexer {indexer.name}")
                        print(f"* Readarr ID {ReadarrIndexer['downloadClientId']} mismatched with {v['readarr']['id']}, updating via API")
                        self.update_indexer(id_=ReadarrIndexer["id"], data = ReadarrIndexer|{ "downloadClientId": v["readarr"]["id"] }, forceSave=True)
        #return message

    def update_indexer(self, id_, data, forceSave: bool):
        force = str(forceSave).lower()
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
            'X-Api-Key': self.api,
        }
        return requests.put(f"{self.host}/api/v1/indexer/{id_}?forceSave={force}", headers = headers, data = json.dumps(data))
        # NOTE: PYARR does not support the force component, I opened an issue https://github.com/totaldebug/pyarr/issues/169
        #self.client.upd_indexer(id_=id_, data=indexer, forceSave=True)

    def message_banner(self):
        print("---------------------------------------------------------------------")
        print("--------------------------PARSING READARR----------------------------")
        print("---------------------------------------------------------------------")