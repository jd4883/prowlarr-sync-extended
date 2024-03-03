class Indexer:
    def __init__(self, download_client_id, enabled, id, name, privacy, protocol, anime_identifiers):
        self.download_client_id = download_client_id
        self.enabled = enabled
        self.id = id
        self.name = name
        self.privacy = privacy
        self.protocol = protocol
        self.anime_keywords = anime_identifiers.get("keywords", ["anime"])
        self.anime_starts_with = anime_identifiers.get("starts_with", ["ani"])
    
    def is_anime(self):
        for keyword in self.anime_keywords:
            if keyword.lower() in self.name.lower():
                return True
        for start_word in self.anime_starts_with:
            if self.name.lower().startswith(start_word):
                return True
        return False
    
    def is_downloader_set(self, downloader):
        return (self.download_client_id==downloader.id)

    def needs_set_public(self, downloader):
        if self.is_downloader_set(downloader):
            return False
        return ((self.privacy=="public") and (downloader.privacy=="public") and (downloader.anime==self.is_anime()))
    
    def needs_set_private(self, downloader):
        if self.is_downloader_set(downloader):
            return False
        return ((self.privacy=="private") and (downloader.privacy=="private") and (downloader.anime==self.is_anime()))

    def needs_set_all(self, downloader):
        if self.is_downloader_set(downloader) and (self.download_client_id==0):
            return False
        return (self.privacy=="private") and (downloader.privacy=="all") and (self.protocol=="usenet")