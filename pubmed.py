import time
from api import API, Params


class PubMedAPI:
    def __init__(self):
        self.__api = API()

    @property
    def api(self):
        return self.__api

    def extract(self, term):
        param = Params(term)  # setting up params
        return self.get_pmids(param)

    def get_pmids(self, param: Params, start_=1):
        result = self.api.get_response(param)
        if result.record_count <= len(result):
            return result

        # take out maximum PMID
        max_pmid = max(result.pmids)

        # divide the PMID into two halves and run API for each half
        param.uid_start = start_
        param.uid_end = (start_ + max_pmid) // 2
        left = self.get_pmids(param, start_)

        param.uid_start = (start_ + max_pmid) // 2
        param.uid_end = max_pmid
        right = self.get_pmids(param, param.uid_start)

        return left + right


if __name__ == '__main__':
    start = time.time()
    p = PubMedAPI()
    e = p.extract('"parkinson\'s disease"')
    # print(e.pmids)
    print(f"PMID Count: {e.record_count}")
    print(f"Time Taken: {time.time() - start}")
