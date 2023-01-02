from typing import Dict, List
from requests import Session
from xmltodict import parse
from datetime import datetime


class ResultSet:
    def __init__(self):
        pass


class Params:
    def __init__(
            self,
            term: str,
            ret_max: int = 10_000,
            min_date=datetime(year=1500, month=1, day=1),
            max_date=datetime.utcnow()
    ):
        self.__term = term
        self.__ret_max = ret_max
        self.__min_date = min_date
        self.__max_date = max_date

    @property
    def min_date(self):
        return self.__min_date

    @min_date.setter
    def min_date(self, new_min):
        self.__min_date += new_min

    @property
    def max_date(self):
        return self.__max_date

    @max_date.setter
    def max_date(self, new_max):
        self.__max_date += new_max


class API(Session):
    __BASE_URL__ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    def __init__(self):
        super(API, self).__init__()

    def get_response(self, **kwargs) -> Dict | List:
        response = self.get(self.__BASE_URL__, **kwargs)
        return parse(response.content)
