import time
from .api import API, Params


class PubMedAPI:
    __PUBMED_LIMIT__ = 10_000

    def __init__(self, years_of_data: int = 500):
        self.__api = API()
        self.__years_of_data = years_of_data  # how many years of data to be fetched. default is 500 years

    @property
    def api(self):
        return self.__api

    def extract(self, term):
        param = Params(term)  # setting up params
        param.change_years_difference(self.__years_of_data)
        return self.get_pmids(param)

    def get_pmids(self, param: Params, start_=1, end_=None):
        """fetches PMIDs recursively"""
        result = self.api.get_response(param)

        # if result count is less than pubmed limit
        if result.record_count < self.__PUBMED_LIMIT__:
            return result

        # take out maximum PMID (only when end_ boundary is not provided in function call)
        if not end_:
            max_pmid = max(result.pmids)
            end_ = max_pmid

        # divide the PMID into two halves and run API for each half
        param.uid_start = start_
        param.uid_end = (start_ + end_) // 2
        left = self.get_pmids(param, start_, param.uid_end)

        param.uid_start = (start_ + end_) // 2
        param.uid_end = end_
        right = self.get_pmids(param, param.uid_start, param.uid_end)

        return left + right

    def close(self):
        """closes the connection with API"""
        self.api.close()
