#from classes.download_client import DownloadClient
from classes.indexer import Indexer
from methods.logging import *
from prowlarr.models.indexer_resource import IndexerResource
import prowlarr


class Prowlarr:
    def __init__(self, api, host):
        self.api = api
        self.host = host
        self.client = self.set_client()
        self.indexer = prowlarr.IndexerApi(self.client)
        self.download_clients = prowlarr.DownloadClientApi(self.client)
        self.indexers = self.get_indexers()
        self.download_client_mappings = dict()
        [self.update_download_clients_mapping(download_client=i, source="prowlarr") for i in self.get_download_clients()]
        
    def set_client(self):
        conf = prowlarr.Configuration(host = self.host)
        api_key = conf.api_key['X-Api-Key'] = conf.api_key['apikey'] = self.api
        return prowlarr.ApiClient(conf)
    
    def get_indexers(self):
        return self.indexer.list_indexer()
    
    def get_download_clients(self):
        return self.download_clients.list_download_client()
    
    def update_download_clients_mapping(self, download_client, source):
        if source=="prowlarr":
            self.download_client_mappings.update({(download_client.name) : { (source) : { "id": download_client.id, "name": download_client.name } } })
        else:
            self.download_client_mappings[download_client["name"]].update({ (source) : { "id": download_client["id"], "name": download_client["name"] } })

    def update_indexer_torrent_client_mapping(
        self, 
        download_client_id, 
        indexer, 
        indexer_id, 
        force_save: True,
        packSeedTime: float, 
        seedRatio: float, 
        seedTime: float, 
    ):
        indexer.download_client_id = download_client_id
        for k, v in indexer:
            if k == "fields":
                for i in v:
                    if i.name == "torrentBaseSettings.seedRatio":
                        i.value=seedRatio    
                    elif i.name == "torrentBaseSettings.seedTime":
                        i.value=seedTime
                    elif i.name == "torrentBaseSettings.packSeedTime":
                        i.value=packSeedTime
        return self.indexer.update_indexer(str(indexer_id), force_save=force_save, indexer_resource=indexer)

    def parse_indexers(self, download_clients, ratios):
        for i in self.indexers:
            self.parse_indexer(
                indexerObject=i, 
                indexer = Indexer(download_client_id = i.download_client_id, enabled = i.enable, id = i.id, name = i.name, privacy = i.privacy.split(".")[0], protocol = i.protocol.split(".")[0]), 
                download_clients = download_clients, 
                ratios = ratios
            )
    
    def parse_indexer(self, indexerObject, indexer, download_clients, ratios):
        for downloader in download_clients:
            result, notification = self.parse_torrent_indexer(downloader=downloader, indexerObject=indexerObject, indexer=indexer, ratios=ratios, download_client_id=downloader.id) if indexer.protocol == "torrent" else self.parse_usenet_indexer(downloader=downloader, indexerObject=indexerObject, indexer=indexer, download_client_id=downloader.id)
            log_print(log=result, level=notification)

    def parse_torrent_indexer(self, downloader, indexerObject, indexer, ratios, download_client_id):
        if indexer.needs_set_all(downloader):
            log_print(f"Need to set indexer to Any for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}")
        elif indexer.needs_set_public(downloader):
            log_print(f"Need to set indexer to public for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}")
            force_save=ratios["public"].get("validation", False)
            indexer_id=str(indexer.id)
            packSeedTime = ratios["public"].get("packSeedTime", 0)
            seedRatio =ratios["public"].get("seedRatio", 0)
            seedTime = ratios["public"].get("seedTime", 0)
            return self.update_indexer_torrent_client_mapping(download_client_id=download_client_id, force_save=force_save, indexer=indexerObject,indexer_id=indexer_id, packSeedTime = packSeedTime, seedRatio =seedRatio, seedTime = seedTime), "info"
        elif indexer.needs_set_private(downloader):
            log_print(f"Need to set indexer to private for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}")
            download_client_id=downloader.id, 
            force_save=ratios["private"].get("validation", True) 
            indexer_id=str(indexer.id)
            packSeedTime = ratios["private"].get("packSeedTime", 80640) 
            seedRatio =ratios["private"].get("seedRatio", 3)
            seedTime = ratios["private"].get("seedTime", 80640)
            return self.update_indexer_torrent_client_mapping(download_client_id=download_client_id, force_save=force_save, indexer=indexerObject,indexer_id=indexer_id, packSeedTime = packSeedTime, seedRatio =seedRatio, seedTime = seedTime), "info"
        else:
            return f"No action needed for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}", "debug"
    
    def parse_usenet_indexer(self, downloader, indexerObject, indexer, download_client_id):
        return "Usenet not implemented", "debug"
        if indexer.needs_set_all(downloader):
            return f"Need to set indexer to Any for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}", "info"
        elif indexer.needs_set_public(downloader):
            return f"Need to set indexer to public for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}", "info"
        elif indexer.needs_set_private(downloader):
            return f"Need to set indexer to private for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}", "info"
        else:
            return f"No action needed for {indexer.name}, {indexer.privacy} and {indexer.protocol}, {indexer.download_client_id}", "info"