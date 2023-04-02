"""
Tests are written on 15th March 2023.
We have PMIDs counts taken on 7th March 2023 (from confluence)
We are expecting PMIDs counts for each search string which ran on 7th March lesser than or equal to today's date.
"""
import unittest
from pubmed_api.pubmed import PubMedAPI


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.pubmed_api = PubMedAPI()

    def test_search_string_chicken_and_dentist_less_than_10k(self):
        """
        search_string: chicken AND dentist
        expected_pmid_count: >= 8
        :return: None
        """
        search_string = "chicken AND dentist"
        result = self.pubmed_api.extract(search_string)
        self.assertLessEqual(8, result.record_count)

    def test_search_string_hair_pain_or_ring_pain_less_than_10k(self):
        """
        search_string: "hair pain" OR "ring pain"
        expected_pmid_count: >= 10
        :return: None
        """
        search_string = '"hair pain" OR "ring pain"'
        result = self.pubmed_api.extract(search_string)
        self.assertLessEqual(10, result.record_count)

    def test_search_string_ankle_modelling_more_than_10k(self):
        """
        search_string: ankle modelling
        expected_pmid_count: >= 10368
        :return: None
        """
        search_string = 'ankle modelling'
        result = self.pubmed_api.extract(search_string)
        self.assertGreaterEqual(result.record_count, 10368)

    def test_search_string_parkinson_disease_more_than_100k(self):
        """
        search_string: "parkinson\'s disease"
        expected_pmid_count: >= 106613
        :return: None
        """
        search_string = '"parkinson\'s disease"'
        result = self.pubmed_api.extract(search_string)
        self.assertGreaterEqual(result.record_count, 106613)

    def test_search_string_human_immunodeficiency_virus_more_than_10k(self):
        """
        search_string: "human immunodeficiency virus (hiv)"
        expected_pmid_count: >= 47164
        :return: None
        """
        search_string = '"human immunodeficiency virus (hiv)"'
        result = self.pubmed_api.extract(search_string)
        self.assertGreaterEqual(result.record_count, 47164)

    def test_search_string_complex_string_more_than_10k(self):
        """
        search_string: ( "Glucocorticoids"[MeSH] OR "Corticosteroids"[TIAB] OR "hydrocortisone"[TIAB] OR
        "dexamethasone"[TIAB] OR "prednisone"[TIAB] OR "cortisone"[TIAB] OR "Corticosteroid"[TIAB] OR "Deltasone"[
        TIAB] OR "Prednisone"[TIAB] OR "Entocort EC"[TIAB:~0] OR "Budesonide"[TIAB] OR "Cortef"[TIAB] OR
        "Hydrocortisone"[TIAB])
        expected_pmid_count: >= 285985
        :return: None
        """
        search_string = '( "Glucocorticoids"[MeSH] OR "Corticosteroids"[TIAB] OR "hydrocortisone"[TIAB] OR ' \
                        '"dexamethasone"[TIAB] OR "prednisone"[TIAB] OR "cortisone"[TIAB] OR "Corticosteroid"[TIAB] ' \
                        'OR "Deltasone"[TIAB] OR "Prednisone"[TIAB] OR "Entocort EC"[TIAB:~0] OR "Budesonide"[TIAB] ' \
                        'OR "Cortef"[TIAB] OR "Hydrocortisone"[TIAB])'
        result = self.pubmed_api.extract(search_string)
        self.assertGreaterEqual(result.record_count, 285985)

    def tearDown(self) -> None:
        self.pubmed_api.close()


if __name__ == '__main__':
    unittest.main()
