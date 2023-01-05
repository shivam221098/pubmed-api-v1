from typing import Dict, List
from requests import Session
from requests.exceptions import ConnectionError, ConnectTimeout
from xmltodict import parse
from datetime import datetime


class ResultSet:
    def __init__(self):
        pass


class Params:
    __BASE_MIN_DATE__ = datetime(year=1500, month=1, day=1)
    __BASE_MAX_DATE__ = datetime.utcnow()

    def __init__(
            self,
            term: str,
            ret_max: int = 10_000,
            min_date: datetime = None,
            max_date: datetime = None
    ):
        self.__term = term
        self.__ret_max = ret_max
        self.__min_date = min_date if min_date is not None else self.__BASE_MIN_DATE__
        self.__max_date = max_date if max_date is not None else self.__BASE_MAX_DATE__

    @property
    def min_date(self):
        """:returns: minimum date"""
        return self.__min_date

    @min_date.setter
    def min_date(self, new_min):
        """sets new minimum date"""
        self.__min_date = new_min

    @property
    def max_date(self):
        """:returns: maximum date"""
        return self.__max_date

    @max_date.setter
    def max_date(self, new_max):
        """sets new maximum date"""
        self.__max_date = new_max

    def to_dict(self, db=None) -> Dict:
        """
        method converts current instance variables into dictionary
        :return: key value pairs that will be used in API call
        """
        parameters = {
            "term": self.__term,
            "retmax": self.__ret_max,
            "mindate": self.min_date.strftime("%Y/%m/%d"),
            "maxdate": self.max_date.strftime("%Y/%m/%d"),
        }
        if db is not None:
            parameters.update({"db": db})

        return parameters


class API(Session):
    __BASE_ESEARCH_URL__ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    __BASE_EFETCH_URL__ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    __MAX_RETRY__ = 2  # number of times to retry API if fails to get any data

    def __init__(self):
        super(API, self).__init__()

    def get_response(self, params: Params, **kwargs) -> Dict | List | None:
        # try first time
        retry_count = 0
        while retry_count < self.__MAX_RETRY__:
            try:
                response = self.get(self.__BASE_ESEARCH_URL__, params=params.to_dict(), **kwargs)
                return parse(response.content)
            except (ConnectionError, ConnectTimeout):
                # second retry
                retry_count += 1
                continue
        return None

    def get_record_count(self, params: Params, **kwargs) -> int | None:
        try:
            search_response = self.get(self.__BASE_ESEARCH_URL__, params=params.to_dict("pubmed"), **kwargs)
            tree = parse(search_response.content)
            return int(tree.get("eSearchResult").get("Count"))
        except (ConnectionError, ConnectTimeout):
            return None
