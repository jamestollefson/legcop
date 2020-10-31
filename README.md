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

```
#import
from legcop.legcop.legiscan import LegiScan

#instantiate LegiScan
api_key = #YOUR API KEY HERE
legis = LegiScan(api_key)

``` 