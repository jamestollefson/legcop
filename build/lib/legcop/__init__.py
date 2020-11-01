import requests
import os
import json
import base64
import zipfile
import io


class LegiScanError(Exception):
    pass

class LegiScan(object):
    BASE_URL = 'https://api.legiscan.com/?key={}&op={}{}'
    
    def __init__(self, apikey=None, mute=False):
        """LegiScan API. State parameters should always be passed as
        USPS abbreviations. Bill numbers and abbreviations are case insensitive.
        Register for API at https://legiscan.com/legiscan
        """
        self.mute = mute
        self.key = apikey
        #See if API key is available as environment variable
        if apikey is None:
            try:
                apikey = os.environ['LEGISCAN_API_KEY']
                self.key = apikey.strip()
            except:
                self.key = ''
                if self.mute == False:
                    print(
                        '''
                        Object has been instantiated. However, you must provide 
                        a valid LegiScan API key to use this object.
    
                        The API key for this object may be set by passing it as an 
                        argument to the set_api_key() method on this object.
                        
                        To obtain an API key, visit https://legiscan.com/legiscan
                        '''                    
                        )
        
        
    def _url(self, operation, params=None):
        """Build a URL for querying the API"""
        if params is not None:
            param_string = ''
            for param, value in params.items():
                param_string += '&{}={}'.format(param, value)
        
        return self.BASE_URL.format(self.key, operation, param_string)
    
    def _get(self, url):
        """Get and parse JSON from API for a url."""
        req = requests.get(url)
        data = json.loads(req.content)
        if data['status'] == 'ERROR':
            raise LegiScanError(data['alert']['message'])
        return data
    
    def set_api_key(self, key):
        """allows user to set API key manually if not done during
            instantiation or available as an environmental variable"""
        self.key = key
    
    def get_session_list(self, state):
        """Get list of all available sessions for a state"""
        url = self._url('getSessionList', {'state': state})
        data = self._get(url)
        return data['sessions']
    
    def get_master_list(self, state=None, session_id=None):
        """Get list of bills for the current session in a state or for a 
            given session identifier"""
            
        if state is not None:
            url = self._url('getMasterList', {'state': state})
        elif session_id is not None:
            url = self._url('getMasterList', {'id':session_id})
        else:
            raise ValueError('Must specify session identifier or state. Do not specify both. If you do only the state will be used in the resulting query')
        data = self._get(url)
        #return a list of the bills
        return [data['masterlist'][i] for i in data['masterlist']]
    
    def get_bill(self, bill_id=None, state=None, bill_number=None):
        """Get primary bill detail information including sponsors, committee
            references, full history, bill text, and roll call information.
            
            This function expects either a bill identifier or a state and bill number 
            combination. The bill identifier is preferred, and required for fetching bills
            from prior sessions.
        """
        if bill_id is not None:
            url = self._url('getBill', {'id':bill_id})
        elif state is not None and bill_number is not None:
            url = self._url('getBill', {'state':state, 'bill':bill_number})
        else:
            raise ValueError('Must specify bill_id OR state and bill_number.')
        return self._get(url)['bill']
    
    def get_bill_text(self, bill_id, use_base64=False):
        """
        Get bill text, including date, draft revision information, and
        MIME type. 
        
        If `use_base64` is False (default) bill text is returned in ASCII for easy
        readability.
        
        Otherwise, text is base64 encoded to allow for PDF and Word 
        data transfers.
        """
        url = self._url('getBillText', {'id':bill_id})
        bill_text = self._get(url)['text']
        if use_base64 == True:
            return bill_text
        else:
            doc = bill_text['doc']
            base64_bytes = doc.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message_bytes.decode('ascii')
            bill_text['doc'] = message
            return bill_text

    def get_amendment(self, amendment_id):
        """
        Get amendment text including date, adoption status, MIME type,
        and title/description information. Amendment text is encoded in
        base64 to allow for PDF and Word data transfers.
        """
        url = self._url('getAmendment', {'id':amendment_id})
        return self._get(url)['amendment']
        
    def get_supplement(self, supplement_id):
        """
        Get supplement text including type of supplement, date, MIME type
        and text description/information. Supplement text is base64 encoded 
        to allow for PDF and Word data transfer.
        """
        url = self._url('getSupplement', {'id':supplement_id})
        return self._get(url)['supplement']
    
    def get_roll_call(self, roll_call_id):
        """Roll call detail for individual votes and summary information."""
        data = self._get(self._url('getRollcall', {'id':roll_call_id}))
        return data['roll_call']
    
    def get_person(self, people_id):
        """Legislator information including name, role, and a followthemoney.org
        person identifier."""
        url = self._url('getSponsor', {'id':people_id})
        return self._get(url)['person']
        
    def search(self, state, bill_number=None, query=None, year=2, page=1):
        """
        Get a page of results for a search against the LegiScan full text 
        engine; returns a paginated result set.
        
        Specify a bill number or query string. Year can be an exact year 
        or a number between 1 and 4, inclusive. These integers have the 
        following meanings:
            1 = all years
            2 = current year, the default
            3 = recent years
            4 = prior years
        Page is the result set page number to return
        """
        if bill_number is not None:
            params = {'state':state,'bill':bill_number}
        elif query is not None:
            params = {'state':state, 'query':query,
                      'year':year, 'page':page}
        else:
            raise ValueError('Must specify bill_number or query')
        data = self._get(self._url('search', params))['searchresult']
        #return a summary for the search and the results as a dictionary
        summary = data.pop('summary')
        results = {'summary':summary, 'results': [data[i] for i in data]}
        return results
    
    def get_dataset_list(self, state=None, year=None):
        """Get a list of available datasets with optional filters"""
        params = {}
        if state is not None:
            params['state'] = state
        if year is not None:
            params['year'] = year
        url = self._url('getDatasetList', params)
        return self._get(url)['datasetlist']
    
    def get_dataset(self, session_id = None, access_key=None):
        """
        Returns a single ZIP archive for the requested dataset containing all bills,
        votes, and people for the selected session.
        
        To get a list of available datasets use the get_dataset_list. Select an access_key
        and session_id from the results to use an inputs for get_dataset().
        """
        if session_id is not None and access_key is not None:
            params = {'id':session_id, 'access_key':access_key}
            url = self._url('getDataset', params)
            return self._get(url)
        else:
            raise ValueError('Provide session_id and access_key')
    
    def get_session_people(self, session_id):
        """Retrieve a list of people records active in a specific session id"""
        url = self._url('getSessionPeople', {'id': session_id})
        return self._get(url)['sessionpeople']['people']
    
    def get_sponsored_list(self, people_id):
        """Retrieve a list of bills sponsored by an individual legislator"""
        url = self._url('getSponsoredList', {'id':people_id})
        return self._get(url)['sponsoredbills']['bills']
    
    def recode_zipfile(self, zipped_dataset):
        """This function re-encodes the zipped dataset produced by the API to make
        it human-readable. 
        
        It then returns a zipfile.Zipfile object. For more information about how to 
        access/manipulate this object, refer to the zipfile docs:
            
        https://docs.python.org/3/library/zipfile.html#zipfile-objects
        """
            
        if zipped_dataset['status'] == 'OK':
            zipped_data = zipped_dataset['dataset']['zip']
            
        else:
            raise LegiScanError('''Dataset status not OK. Try pulling the dataset 
                    again using get_dataset(). To get a list of datasets for a 
                    given state, use the get_dataset_list() method on a LegiScan 
                    instance.
                    
                    get_dataset_list returns a list of datasets (makes sense, 
                    right?). Once you identify the one you are interested in get,
                    its access_key and session_id and pass them as arguments to 
                    get_dataset().
                    
                    Here's an example:
                        
                    #instantiate LegiScan
                    api_key = #Your API Key Here
                    legis = LegiScan(api_key)
                    datasetlist = legis.get_dataset_list(state='ak', year=2019)
                    #get access_key and session_id from first list item
                    access_key = datasetlist[0]['access_key']
                    session_id = datasetlist[0]['session_id']
                    
                    #get dataset
                    dataset = legis.get_dataset(session_id=session_id,
                                                access_key=access_key)
                    
                    #check to make sure dataset status is 'OK'
                    assert dataset['status'] == 'OK'
                    
                    #Now you can use recode_zipfile to make this readable
                    readable = legis.recode_zipfile(dataset)
                        ''')
    
        #re-encode
        base64_bytes = zipped_data.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        
        recoded_zipfile = zipfile.ZipFile(io.BytesIO(message_bytes))
        
        return recoded_zipfile
    
    def __str__(self):
        return '<LegiScan API key: {}'.format(self.key)
    
    def __repr__(self):
        return str(self)