import os
import unittest

from atomicwrite import atomic_write

@atomic_write
def my_writer(content, file, mode='wb', encoding=None):
    pass

class AtomicWriteTest(unittest.TestCase):
    def setUp(self):
        self.parquet_file = './userdata1.parquet'
        self.saved_file = './res.parquet'
    
    
    def test_parquet_file(self):
        
        f = open(self.parquet_file, 'rb')
        data = f.read()
        f.close()
        my_writer(content=data, file=self.saved_file, mode='wb')
        
        f = open(self.saved_file, "rb")
        res = f.read()
        f.close()
        try:
            self.assertEqual(data, res)
        finally:
            os.remove(self.saved_file)

     
if __name__ == "__main__":
    unittest.main()