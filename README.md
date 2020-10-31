# legcop (Legislature Common Operating Picture)

---

This package provides python libraries to interact with various APIs containing information
about legislative activity in the U.S. Congress and the 54 States & Territories.

You can install legcop using `pip install legcop`

### LEGISCAN

---

The venerable LegiScan API provides access to the legislative activity of the U.S. State
and Federal Legislatures. 

Use of the LegiScan API requires an API key which you may obtain for free at 
https://legiscan.com/legiscan.

To learn more about LegiScan's internal functionality you can always peruse the 
user manual/documentation at https://legiscan.com/gaits/documentation/legiscan.

We interact with LegiScan using `LegiScan` objects.

```json
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

```
state = 'ak'
sessions = legis.get_session_list(state=state)

print(sessions)

```

