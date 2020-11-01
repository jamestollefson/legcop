import unittest
import argparse
import os
import requests

from legcop import LegiScan, LegiScanError


class LegiScanTestCase(unittest.TestCase):
    
    def setUp(self):
        self.key = os.environ.get('LEGISCAN_API_KEY')
        self.legis = LegiScan(self.key)
        
    def test_instantiate_API(self):
        """attempt to instantiate LegiScan successfully"""
        try:
            results = self.legis.get_session_list('ak')
            del results
        except:
            self.fail('LegiScan object failed during instantiation')

    def test_url(self):
        """determine in urls created by _url() return 200 HTML responses"""
        url = self.legis._url('getSessionList', {'state': 'ak'})
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "HTTP response did not return 200 code")
        
    def test_get(self):
        """deliberately use incorrect url"""
        url = self.legis._url('getSessionList', {'state': 'kk'})[:-13]
        with self.assertRaises(LegiScanError):
            results = self.legis._get(url)
            del results
            
    def test_get_no_args(self):
        """check that exception is raised when no arguments are passed"""
        with self.assertRaises(Exception):
            self.legis._get()
            
    def test_get_master_list(self):
        """check that exception is raised when neither state nor session_id
        are provided"""
        with self.assertRaises(ValueError):
            self.legis.get_master_list()
            
    def test_get_master_list_args(self):
        """check that an exception is raised when no arguments are provided"""
        with self.assertRaises(ValueError):
            self.legis.get_master_list()
            
    def test_get_bill_state_only(self):
        """check that ValueError is raised when only state is provided as an 
        argument"""
        with self.assertRaises(ValueError):
            self.legis.get_bill(state='ak')
            
    def test_get_bill_number_only(self):
        """check that ValueError is raised when only bill number is provided as
        an argument"""
        with self.assertRaises(ValueError):
            self.legis.get_bill(bill_number=4512)
                   
    def test_get_bill_id_only(self):
        """check that function returns successfully when only bill id is 
        provided"""
        bill_id = 50
        result = self.legis.get_bill(bill_id=bill_id)
        self.assertEqual(result['bill_id'], bill_id)
        
    def test_get_bill_no_args(self):
        """check that ValueError is raised when no argumets are provided"""
        with self.assertRaises(ValueError):
            self.legis.get_bill()
        
    def test_get_bill_text_no_args(self):
        """check that exception is raised when user fails to specify keyword
        arguments to function"""
        with self.assertRaises(TypeError):
            self.legis.get_bill_text()
            
    def test_recode_zipfile(self):
        """test that the Zipfile object returned by recode_zipfile() passes the
        zipfile testzip() test"""
        
        datasetlist = self.legis.get_dataset_list(state='ak', year=2019)
        #get access_key and session_id from first list item
        access_key = datasetlist[0]['access_key']
        session_id = datasetlist[0]['session_id']
        
        #get dataset
        dataset = self.legis.get_dataset(session_id = session_id,
                                         access_key = access_key)
        
        #Ensure dataset status is ok
        assert dataset['status'] == 'OK'
        
        #pass dataset to recode_zipfile()
        readable = self.legis.recode_zipfile(dataset)
        
        self.assertEqual(type(readable.testzip()), type(None))

                    
    def test_get_dataset(self):
        """Check that result status is 'OK' for dataset known to exist in DB"""
        
        datasetlist = self.legis.get_dataset_list(state='ak', year=2019)
        #get access_key and session_id from first list item
        access_key = datasetlist[0]['access_key']
        session_id = datasetlist[0]['session_id']
        
        #get dataset
        dataset = self.legis.get_dataset(session_id = session_id,
                                         access_key = access_key)
        self.assertEqual(dataset['status'], 'OK')
        
        pass
            
     
if __name__ == '__main__':
    
    print(
        '''
        Running this test package requires an API key for LegiScan.
        
        To obtain an API key, visit https://legiscan.com/legiscan
        '''
        )
    
    key = input("LegiScan API Key: ")
    os.environ['LEGISCAN_API_KEY'] = key
    
    unittest.main()
