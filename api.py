from typing import Dict, List
from requests import Session
from requests.exceptions import ConnectionError, ConnectTimeout
from xmltodict import parse
from datetime import datetime


class ResultSet:
    def __init__(self, pmids=None, record_count: int = 0):
        if pmids is None:
            pmids = []

        if isinstance(pmids, list):
            self.__pmids = list(map(int, pmids))
        elif isinstance(pmids, str):
            self.__pmids = [int(pmids)]
        else:
            self.__pmids = pmids
        self.__record_counts = record_count

    @property
    def pmids(self):
        return self.__pmids

    @property
    def record_count(self):
        return self.__record_counts

    @record_count.setter
    def record_count(self, new):
        self.__record_counts = new

    def __len__(self):
        return len(self.pmids)

    def __add__(self, other):
        self.pmids.extend(other.pmids)
        self.record_count += other.record_count
        return self


class Params:
    def __init__(
            self,
            term: str,
    ):
        self.__term = term
        self.__retstart = 0
        self.__uid_start = 1
        self.__uid_end = None

    @property
    def uid_start(self):
        return self.__uid_start

    @uid_start.setter
    def uid_start(self, new):
        self.__uid_start = new

    @property
    def uid_end(self):
        return self.__uid_end

    @uid_end.setter
    def uid_end(self, new):
        self.__uid_end = new

    def to_dict(self):
        if not self.uid_end:
            # initial call param to get the largest pmid from the corpus
            return {
                "term": self.__term,
                "retmax": 9999,
                "retstart": 0
            }
        return {
            "term": self.__term + f" AND {self.uid_start}:{self.uid_end}[UID]",
            "retmax": 9999,
            "retstart": 0
        }


class API(Session):
    __BASE_ESEARCH_URL__ = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    __MAX_RETRY__ = 2  # number of times to retry API if fails to get any data
    __HEADERS__ = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36"
    }

    def __init__(self):
        super(API, self).__init__()

    def get_response(self, params: Params, **kwargs) -> ResultSet:
        # trying first time
        retry_count = 0
        while retry_count < self.__MAX_RETRY__:
            try:
                response = self.get(self.__BASE_ESEARCH_URL__, params=params.to_dict(), headers=self.__HEADERS__,
                                    **kwargs)
                return self.parse_xml(parse(response.content))
            except (ConnectionError, ConnectTimeout):
                print("Retrying...")
                # second retry
                retry_count += 1
                continue
        return ResultSet()

    def parse_xml(self, content: Dict) -> ResultSet:
        print(content)
        try:
            pmids = content.get("eSearchResult", {}).get("IdList", {}).get("Id")
            return ResultSet(pmids, self.get_result_count(content))
        except AttributeError:
            return ResultSet()

    @staticmethod
    def get_result_count(content: Dict) -> int:
        return int(content.get("eSearchResult", {}).get("Count", '0'))


if __name__ == '__main__':
    p = Params('"parkinson\'s disease" 1:1[UID]')
    a = API()
    print(a.get_response(p).pmids)