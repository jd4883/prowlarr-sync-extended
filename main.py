from classes.prowlarr import Prowlarr
from classes.sonarr import Sonarr
from classes.download_client import DownloadClient
from os import getenv
from pyarr import LidarrAPI
from pyarr import RadarrAPI
from pyarr import ReadarrAPI
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


if __name__ == '__main__':
    config = get_config("config.yaml")
    prowlarr = Prowlarr(api=getenv("PROWLARR_API", ""),host=getenv("PROWLARR_HOST", "http://localhost:9696"))
    download_clients = set_download_clients(config.pop("download_clients"), prowlarr.get_download_clients())
    sonarr = Sonarr(api=getenv("SONARR_API", ""),host=getenv("SONARR_HOST", "http://localhost:9696"), download_clients = download_clients)
    prowlarr.parse_indexers(
        download_clients = download_clients,
        ratios = config.pop("ratios"),
    )
    
    # [self.update_download_clients_mapping(download_client=i, source="sonarr") for i in sonarr.download_clients]
    #     from pprint import pprint 
    #     pprint(self.download_clients)
    #     pprint(sonarr.download_clients)
    # for i in sonarr.download_clients:
            
    #         pprint(sonarr.get_download_client_id(i))
    #         breakpoint()
    #         pprint(i.id)
        
    # sonarr_indexers = []
    #     for i in sonarr.indexers:
    #         name = i["name"].replace(" (Prowlarr)", "")
    #         privacy = ""
    #         for j in self.indexers:
    #             if j.name == name:
    #                 privacy = j.privacy.split(".")[0]
    #                 break
                
    #         indexer = Indexer(
    #             download_client_id = i["downloadClientId"], 
    #             enabled = True, 
    #             id = i["id"], 
    #             name = i["name"].replace(" (Prowlarr)", ""), 
    #             privacy = privacy,
    #             protocol = i["protocol"],
    #         )
    #         #i["downloadClientId"] = 
    #         breakpoint()
    #         #upd_indexer(id = indexer.id)
    #         sonarr_indexers.append(indexer)
        
    #     breakpoint()
    #     # TODO: update indexers and make method as clean and generic as possible
        
    
        
    
    
    
    