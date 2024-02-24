class Indexer:
    def __init__(self, download_client_id, enabled, id, name, privacy, protocol):
        self.download_client_id = download_client_id
        self.enabled = enabled
        self.id = id
        self.name = name
        self.privacy = privacy
        self.protocol = protocol
    
    def needs_set_public(self, downloader):
        return (self.privacy=="public") and (self.download_client_id!=downloader.id) and (downloader.privacy=="public")
    
    def needs_set_private(self, downloader):
        return (self.privacy=="private") and (self.download_client_id!=downloader.id) and (downloader.privacy=="private")

    def needs_set_all(self, downloader):
        return (self.privacy=="private") and (self.download_client_id!=0) and (downloader.privacy=="all") and (self.protocol=="usenet")