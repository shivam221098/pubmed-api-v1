# Problem Statement

Due to recent changes in PubMed API policies, they don't allow users get more than 10k results, resulting 
in results capping against search strings.

# Solution #1
1. `edirect` - edirect is a command-line utility. It provides capabilities of fetching PMIDs against a 
search string when `esearch` and `efetch` commands are piped together.

# Solution #2
1. Running pubmed API on search strings with some date-ranges. But sometimes even a single day has more than 10k PMIDs

# Solution #3

Instead of using `edirect` or concept of date-ranges, let's divide the search strings results in ranges of PMIDs.

#### Algorithm
1. Take a usual string and run over PubMed API using `sort=pub_date`. It will get some PMIDs and Count of actual PMIDs from the pubmed db.
2. The returned results are sorted on the basis of most recent articles as we have used `sort=pub_date`. In essence, the most recent PMID is
returned in the very first API call. So, take the maximum PMID from the batch of 10K PMIDs as this PMID is the most is most recent.
3. If the returned PMIDs count (counted PMIDs from response) <= actual counts `<Counts>47851</Counts>` mentioned in the API response. Then our first API call is the required result.
4. If not `Step 3` and current call is first API call, then divide the maximum PMID from `Step 2` by `2`. It will give you two halves. 
First from `1` to `max_pmid / 2` and second from `max_pmid / 2` to `max_pmid`
5. If not `Step 3` and current call is 2nd, 3rd or so on. API call then divide `end` by 2 and make two halves
First from `1` to `end / 2` and second from `end / 2` to `end`
6. Now, change the original search string as follows:

Suppose `max_pmid = 15000` or `end = 15000` (`end` is `null` during first API call. It is initialised with `max_pmid / 2` during 1st API call
and used in all subsequent recursive API calls)

**NOTE: we are only using `max_pmid` in first API call. In all subsequent call we're just making half of `max_pmid` again and again.**

Suppose our search string is `"human immunodeficiency virus (hiv)"`, so, two new search strings will be
`"human immunodeficiency virus (hiv)" AND 1:7500[UID]` and `"human immunodeficiency virus (hiv)" AND 7500:15000[UID]`
For 1st half 
make `start` = `1`
     `end` = `7500`
For 2nd half
make `start` = `7500`
     `end` = `15000`
Now, Run these two string over the API and repeat `Step 3` for each new string.

This way we can grab all PMIDs using API, without shifting to any other new tool.

If you see we are dividing each sets into two halves recursively. That means PMIDs from range `1` to `x` can be fetched
in an API call and the minimum `x` can go is `1`. We are using same concept of date ranges but dividing sets into halves
using PMID itself. This way the issue of more than 10k PMIDs in a day can be corrected, and it's far simpler than
using `edirect` on the terminal. 

The above process takes only `41 Seconds` for `106K` PMIDs.

#### The edirect actually uses the PubMed API to get the results, but how it is able to get the results from PubMed API if it is using the same API? 🤔
#### Actually it uses the same above concept to get the results from API. 🎉


# Usage
### To get PMIDs for a search string
```python
from pubmed_api.pubmed import PubMedAPI


pa = PubMedAPI()  # instantiate once and use it for n number of search terms
# pa = PubMedAPI(10)  # pass any number. This number tells API to fetch only last 10 years of PMIDs
# pa.__PUBMED_LIMIT__ = 100_000  # update with new pubmed limit

search_terms = [
    '"parkinson\'s disease"',
    '"human immunodeficiency virus (hiv)"'
]

for term in search_terms:
    result = pa.extract(term)  # result will the object of ResultSet()
    print(result.pmids)  # will return list of PMIDs (list)
    print(result.record_count)  # will return number if PMIDs (int)
```
