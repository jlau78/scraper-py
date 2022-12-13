import logging
from utils.extractor.extractor import extractor

class api_extractor(extractor):

    def __init__(self) -> None:
        super().__init__()

    def extract(self, source):
        logging.warn('api_extractor has not been implemented yet')
        return super().handle()

