from typing import Dict, List
from requests import Session
from xmltodict import parse


class API(Session):
    __BASE_URL__ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    def __init__(self):
        super(API, self).__init__()

    def get_response(self, **kwargs) -> Dict | List:
        response = self.get(self.__BASE_URL__, **kwargs)
        return parse(response.content)
