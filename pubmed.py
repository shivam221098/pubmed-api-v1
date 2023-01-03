from api import API, Params
from datetime import datetime
from dateutil.relativedelta import relativedelta


class PubMedAPI:
    __RET_MAX__ = 10_00_000

    def __init__(self):
        self.__api = API()

    def get_pmids(self, search_term):
        results = []
        # starting from a points and trying to fetch data in chunks of 100 years

        for i in range(5):
            start_date = Params.__BASE_MIN_DATE__ + relativedelta(years=i * 100)
            end_date = Params.__BASE_MIN_DATE__ + relativedelta(years=(i + 1) * 100)

            params = Params(search_term, self.__RET_MAX__, start_date, end_date)



        # self.__api.get_response()


if __name__ == '__main__':
    p = PubMedAPI()
    print(p.get_pmids("Hello"))