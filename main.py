from classes.download_client import DownloadClient
from classes.lidarr import Lidarr
from classes.prowlarr import Prowlarr
from classes.radarr import Radarr
from classes.readarr import Readarr
from classes.sonarr import Sonarr
from os import getenv
import yaml


def get_config(config):
	return yaml.load(open(config), Loader=yaml.FullLoader)

def set_download_clients(config, downloaders):
    download_clients = []
    for i in config:
        dl = DownloadClient(i)
        dl.parse_downloaders(downloaders)
        download_clients.append(dl)
    return download_clients

def lidarr(prowlarr, download_clients):
    lidarr = Lidarr(api=getenv("LIDARR_API", ""),host=getenv("LIDARR_HOST", "http://localhost:8686"), download_clients = download_clients)
    [prowlarr.update_download_clients_mapping(download_client=i, source="lidarr") for i in lidarr.download_clients]
    lidarr.message_banner()
    [lidarr.parse_indexer_discrepancies(indexer=prowlarrIndexer, download_client_mappings=prowlarr.download_client_mappings) for prowlarrIndexer in prowlarr.indexers]

def sonarr(prowlarr, download_clients):
    sonarr = Sonarr(api=getenv("SONARR_API", ""),host=getenv("SONARR_HOST", "http://localhost:9696"), download_clients = download_clients)
    [prowlarr.update_download_clients_mapping(download_client=i, source="sonarr") for i in sonarr.download_clients]
    sonarr.message_banner()
    [sonarr.parse_indexer_discrepancies(indexer=prowlarrIndexer, download_client_mappings=prowlarr.download_client_mappings) for prowlarrIndexer in prowlarr.indexers]

def radarr(prowlarr, download_clients):
    radarr = Radarr(api=getenv("RADARR_API", ""),host=getenv("RADARR_HOST", "http://localhost:7878"), download_clients = download_clients)
    [prowlarr.update_download_clients_mapping(download_client=i, source="radarr") for i in radarr.download_clients]
    radarr.message_banner()
    [radarr.parse_indexer_discrepancies(indexer=prowlarrIndexer, download_client_mappings=prowlarr.download_client_mappings) for prowlarrIndexer in prowlarr.indexers]

def readarr(prowlarr, download_clients):
    readarr = Readarr(api=getenv("READARR_API", "e4913b5299d3464fb8ce2dbdb1251531"),host=getenv("READARR_HOST", "http://localhost:8787"), download_clients = download_clients)
    [prowlarr.update_download_clients_mapping(download_client=i, source="readarr") for i in readarr.download_clients]
    readarr.message_banner()
    [readarr.parse_indexer_discrepancies(indexer=prowlarrIndexer, download_client_mappings=prowlarr.download_client_mappings) for prowlarrIndexer in prowlarr.indexers]


if __name__ == '__main__':
    config = get_config("config.yaml")
    prowlarr = Prowlarr(api=getenv("PROWLARR_API", ""),host=getenv("PROWLARR_HOST", "http://localhost:9696"))
    download_clients = set_download_clients(config.pop("download_clients"), prowlarr.get_download_clients())
    prowlarr.parse_indexers(download_clients = download_clients, ratios = config.pop("ratios"))    


    sonarr(prowlarr=prowlarr, download_clients=download_clients)
    radarr(prowlarr=prowlarr, download_clients=download_clients)
    lidarr(prowlarr=prowlarr, download_clients=download_clients)
    readarr(prowlarr=prowlarr, download_clients=download_clients)
    
    
        