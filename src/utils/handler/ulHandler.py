import logging
from utils.handler.handler import handler

class ulHandler(handler):

    def __init__(self) -> None:
        super().__init__()


    def handle(self, elements , page_config):
        logging.warn('ulHandler has not been implemented yet')
        return super().handle()

