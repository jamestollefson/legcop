import unittest

#import legiscan

class TestFail(unittest.TestCase):
    def test_fail(self):
        self.assertEqual(9, 7, "should be false")
        
    def test_pass(self):
        self.assertEqual(9, 9, "should be true")
        
if __name__ == '__main__':
    unittest.main()
    
    
    
    