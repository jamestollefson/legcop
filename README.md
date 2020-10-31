# legcop 

The `legcop` (Legislature Common Operating Picture) package provides python libraries to interact with various APIs containing information
about legislative activity in the U.S. Congress and the 54 States & Territories.

You can install legcop using `pip install legcop`

## Table of Contents

1. [Example](#example)

## LEGISCAN

The LegiScan API provides access to the legislative activity of the U.S. State
and Federal Legislatures. 

Use of the LegiScan API requires an API key which you may obtain for free at 
https://legiscan.com/legiscan.

To learn more about LegiScan's internal functionality you can always peruse the 
user manual/documentation at https://legiscan.com/gaits/documentation/legiscan.

We interact with LegiScan using `LegiScan` objects.

```python
#import
from legcop.legcop.legiscan import LegiScan

#instantiate LegiScan
api_key = #YOUR API KEY HERE
legis = LegiScan(api_key)

``` 

The `LegiScan` object provides functions to interact with each of the API
endpoints defined in the https://legiscan.com documentation. The best way to learn
what the API offers is to simply start exploring. A good place to start is with
the list of all available legislative sessions for a particular state.

Let's take a look at what's available for Alaska. Bear in mind that LegiScan
expects postal abbreviations for the state name, and therefore so does this
package.

```python
state = 'ak'
ak_sessions = legis.get_session_list(state=state)

print(ak_sessions)

```

This prints the following:

```
[{'session_id': 1622, 'state_id': 2, 'year_start': 2019, 'year_end': 2020, 'special': 0, 
    'session_name': '31st Legislature', 'name': '31st Legislature', 
    'session_hash': '38cb885fdbd4f65551b7f55c887da845', 'push_safe': 0}, 
{'session_id': 1397, 'state_id': 2, 'year_start': 2017, 'year_end': 2018, 
    'special': 0, 'session_name': '30th Legislature', 'name': '30th Legislature', 
    'session_hash': '4d7b98daa30b3e4459ae14d6b288a301', 'push_safe': 1}, 
{'session_id': 1117, 'state_id': 2, 'year_start': 2015, 'year_end': 2016, 
    'special': 0, 'session_name': '29th Legislature', 'name': '29th Legislature', 
    'session_hash': '49a2faf62f731cb5d6bd0e67689d2045', 'push_safe': 1}, 
{'session_id': 991, 'state_id': 2, 'year_start': 2013, 'year_end': 2014, 
    'special': 0, 'session_name': '28th Legislature', 'name': '28th Legislature', 
    'session_hash': 'c20fa4dfbc1f76119875f11ec6eed813', 'push_safe': 1}, 
{'session_id': 122, 'state_id': 2, 'year_start': 2011, 'year_end': 2012, 
    'special': 0, 'session_name': '27th Legislature', 'name': '27th Legislature', 
    'session_hash': 'b8b0ebf9519f5ff319453b5ac136bbfa', 'push_safe': 1}, 
{'session_id': 58, 'state_id': 2, 'year_start': 2009, 'year_end': 2010, 
    'special': 0, 'session_name': '26th Legislature', 'name': '26th Legislature', 
    'session_hash': '0a97bd55407d490f885805d7f7eee984', 'push_safe': 1}]
```

As you can see, each session comes with a `session_id`, `year_start`, and 
`year_end`. Using this information we can choose a session and pull the list of 
associated datasets from the API.

For this example we'll simply look at the most recent session, which is at index
`0` in the `ak_sessions` list.

```python
#get start year of most recent Alaska Legislature session
start_most_recent_session = ak_sessions[0]['year_start']

#get access key for most recent session
datasetlist = legis.get_dataset_list(state=state, 
                                     year=start_most_recent_session)

#assign the associated access_key and session_id to variables
access_key = datasetlist[0]['access_key']
session_id = datasetlist[0]['session_id']
```

Now that we have the `access_key` and `session_id` for the legislative session
we're interested in we can pull the full dataset from the API.

```python
#pull dataset
dataset = legis.get_dataset(session_id=session_id, access_key=access_key)

#assert that the dataset is good to go
assert dataset['status'] == 'OK'
```

The API returns a zipped, non-human-readable file. `LegiScan` provides a 
convenient method for translating this into a human-readable zipfile.

```
readable_dataset = legis.recode_zipfile(dataset)
```

You now have a `zipfile.ZipFile` object. To learn more about the available 
methods on this object have a look at the documentation at 
https://docs.python.org/3/library/zipfile.html. 

Here's an example of how to read the contents of one of the zipped files using
 `zipfile`.

```python
#get list of all filenames in the dataset
namelist = readable_dataset.namelist()

#select one
item = namelist[0]
content = readable_dataset.read(item)

#convert this from bytes to python dict
import json
content = content.decode('UTF-8')
content = json.loads(content)

for key, value in content['bill'].items():
    print('{}: {}'.format(key, value))
```

This prints out the following for Alaska House Bill 1:

```
bill_id: 1146445
change_hash: 1b8cdc5d7c7e19020f3b215db7f2abed
session_id: 1622
session: {'session_id': 1622, 'session_name': '31st Legislature', 
        'session_title': '31st Legislature', 'year_start': 2019, 
        'year_end': 2020, 'special': 0}
url: https://legiscan.com/AK/bill/HB1/2019
state_link: http://www.akleg.gov/basis/Bill/Detail/31?Root=HB1
completed: 0
status: 1
status_date: 2019-02-20
progress: [{'date': '2019-02-20', 'event': 1}, {'date': '2019-02-20', 'event': 9}]
state: AK
state_id: 2
bill_number: HB1
bill_type: B
bill_type_id: 1
body: H
body_id: 13
current_body: H
current_body_id: 13
title: License In-home Care Providers/agencies
description: An Act relating to the Department of Health and Social Services; 
            relating to in-home personal care services agencies; establishing 
            the In-Home Personal Care Services Advisory Board; and providing 
            for an effective date.
committee: {'committee_id': 2134, 'chamber': 'H', 'chamber_id': 13, 
            'name': 'Health & Social Services'}
pending_committee_id: 2134
history: [{'date': '2019-02-20', 'action': 'PREFILE RELEASED 1/7/19', 
            'chamber': 'H', 'chamber_id': 13, 'importance': 0}, 
        {'date': '2019-02-20', 'action': 'READ THE FIRST TIME - REFERRALS', 
            'chamber': 'H', 'chamber_id': 13, 'importance': 1}, 
        {'date': '2019-02-20', 'action': 'HSS, L&C', 'chamber': 'H', 
            'chamber_id': 13, 'importance': 0}, 
        {'date': '2019-02-20', 'action': 'REFERRED TO HEALTH & SOCIAL SERVICES', 
            'chamber': 'H', 'chamber_id': 13, 'importance': 1}]
sponsors: [{'people_id': 19096, 'person_hash': 'q63acg3w', 'party_id': 2, 
            'party': 'R', 'role_id': 1, 'role': 'Rep', 'name': 'DeLena Johnson', 
            'first_name': 'DeLena', 'middle_name': 'M.', 'last_name': 'Johnson', 
            'suffix': '', 'nickname': '', 'district': 'HD-011', 'ftm_eid': 9405351, 
            'votesmart_id': 153695, 'opensecrets_id': '', 'knowwho_pid': 499617, 
            'ballotpedia': 'Delena_Johnson', 'sponsor_type_id': 1, 
            'sponsor_order': 1, 'committee_sponsor': 0, 'committee_id': '0'}]
sasts: []
subjects: [{'subject_id': 4508, 'subject_name': 'Disabilities'}, 
           {'subject_id': 4478, 'subject_name': 'Licensing'}, 
           {'subject_id': 4545, 'subject_name': 'Medical Care'}, 
           {'subject_id': 4552, 'subject_name': 'Occupations & Professions'}, 
           {'subject_id': 4481, 'subject_name': 'Senior Citizens'}]
texts: [{'doc_id': 1844262, 'date': '2019-01-07', 'type': 'Introduced', 
        'type_id': 1, 'mime': 'application/pdf', 'mime_id': 2, 
        'url': 'https://legiscan.com/AK/text/HB1/id/1844262', 
        'state_link': 'http://www.akleg.gov/PDF/31/Bills/HB0001A.PDF', 
        'text_size': 497807}]
votes: []
amendments: []
supplements: []
calendar: []
```

It may be the case that you have a very specific item of interest and don't want
to pull down an entire legislative session's dataset. legiscan.com provides
convenient API calls to meet this need. For each of these, `LegiScan` provides 
an associated function. 

##### `get_session_list(state)`

Get list of all available sessions for a state

##### `get_master_list(state=None, session_id=None)`

Get list of bills for the current session in a state or for a given session 
identifier

##### `get_bill(bill_id=None, state=None, bill_number=None)`

Get primary bill detail information including sponsors, committee references, 
full history, bill text, and roll call information.

This function expects either a bill identifier or a state and bill number 
combination. The bill identifier is preferred, and required for fetching bills
from prior sessions.


##### `get_bill_text(bill_id, use_base64=False)`

Get bill text, including date, draft revision information, and MIME type. 

If `use_base64` is False (default) bill text is returned in ASCII for easy
readability.

Otherwise, text is base64 encoded to allow for PDF and Word 
data transfers.

##### `get_amendment(amendment_id)`

Get amendment text including date, adoption status, MIME type, and 
title/description information. Amendment text is encoded in base64 to allow for
PDF and Word data transfers.
 
##### `get_supplement(supplement_id)`

Get supplement text including type of supplement, date, MIME type and text 
description/information. Supplement text is base64 encoded to allow for PDF and 
Word data transfer.

##### `get_roll_call(roll_call_id)`

Roll call detail for individual votes and summary information.

##### `get_person(people_id)`

Legislator information including name, role, and a followthemoney.org person 
identifier.

##### `search(state, bill_number=None, query=None, year=2, page=1)`

Get a page of results for a search against the LegiScan full text engine; 
returns a paginated result set.

Specify a bill number or query string. Year can be an exact year or a number 
between 1 and 4, inclusive. These integers have the following meanings:
    1 = all years
    2 = current year, the default
    3 = recent years
    4 = prior years
Page is the result set page number to return

##### `get_dataset_list(state=None, year=None)`

Get a list of available datasets with optional filters

##### `get_dataset(session_id = None, access_key=None)`

Returns a single ZIP archive for the requested dataset containing all bills,
votes, and people for the selected session.

To get a list of available datasets use `get_dataset_list()`. Select an 
`access_key` and `session_id` from the results to use an inputs for 
`get_dataset()`.

##### `get_session_people(session_id)`

Retrieve a list of people records active in a specific session id

##### `get_sponsored_list(people_id)`

Retrieve a list of bills sponsored by an individual legislator

##### `recode_zipfile(zipped_dataset)`

This function re-encodes the zipped dataset produced by the API to make it 
human-readable. 

It then returns a zipfile.Zipfile object. For more information about how to 
access/manipulate this object, refer to the zipfile docs:
    
https://docs.python.org/3/library/zipfile.html#zipfile-objects

## Example

 










