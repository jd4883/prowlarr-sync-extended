from methods.logging import *
import logging


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
)
logging.Formatter("[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")


class DownloadClient:
    def __init__(self, downloadClient):
        self.name = downloadClient.pop("name")
        self.enabled = downloadClient.pop("enabled")
        self.hostname = downloadClient.pop("hostname")
        self.port = downloadClient.pop("port")
        self.privacy = downloadClient.pop("privacy")
        self.protocol = downloadClient.pop("protocol")
        self.id = int()
    
    def parse_downloaders(self, downloaders):
        for d in downloaders:
            if d.name == self.name:
                self.id = d.id
                if d.enable != self.enabled:
                    logging.info(f"Downlodaer {self.name} has a configuration mismatch, handling to be added")
                break