# legcop 

The `legcop` (Legislature Common Operating Picture) package provides python libraries to interact with various APIs containing information
about legislative activity in the U.S. Congress and the 54 States & Territories.

You can install legcop using `pip install legcop`

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
endpoints defined in the legiscan.com documentation. The best way to learn
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
readable_dataset.read(item)
```

It may be the case that you have a very specific item of interest and don't want
to pull down an entire legislative session's dataset. legiscan.com provides
convenient API calls to meet this need. For each of these, `LegiScan` provides 
an associated function. 

##### `get_master_list()`

This returns a list of all bills for either a state or a particular session, 
depending on which arguments you specify in the function call.

```python

```