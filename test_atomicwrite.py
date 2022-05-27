import os
import unittest
import codecs
from atomicwrite import atomic_write


def create_file(file, content=b'Hello World\n', chmode=None):
    '''Atomic write content to file
    
    :param file: str, the destination file path 
    :param content: str, the file content
    :param chmode: optional str, the ownership permission
    '''
    with open(file, 'wb') as f:
        f.write(content)
    if chmode:
        os.chmod(file, chmode)

        
@atomic_write
def my_writer(content, file, mode='wb', encoding=None):
    '''Atomic write content to file
    
    :param content: str, the file content
    :param file: str, the destination file path 
    :param mode: str, the file mode for the temporary file
    :param encoding: optional str, the encoding method
    '''
    pass


class AtomicWriteTest(unittest.TestCase):
    def setUp(self):
        self.file = './res.txt'
        self.content = b'Atomic Write Test.\n'
        self.mode = 'wb'
    
    
    def test_atomic_write(self):
        create_file(self.file)
        my_writer(content=self.content, file=self.file, mode=self.mode)
        
        f = open(self.file, "rb")
        res = f.read()
        f.close()
        try:
            self.assertEqual(res, self.content)
        finally:
            os.remove(self.file)
        
        
    def test_close(self):
        create_file(self.file)
        my_writer(content=self.content, file=self.file, mode=self.mode)
        
        try:
            f = open(self.file, "wb")
            f.write(self.content)
            f.close()
        except:
            self.fail('ValueError raised')
            
        finally:
            os.remove(self.file)
        
    
    def test_permission(self):
        
        test_mode = 0o741
        create_file(self.file, chmode=test_mode)
        my_writer(content=self.content, file=self.file, mode=self.mode)

        st_mode = os.lstat(self.file).st_mode & 0o777
        try:
            self.assertEqual(st_mode, test_mode)
        finally:
            os.remove(self.file)
            
            
    def test_encoding(self):
        data = u'Atomic Write Test.\n'
        my_writer(content=data, file=self.file, mode=self.mode, encoding='utf-8')

        f = codecs.open(self.file, "rb", encoding='utf-8')
        result = f.read()
        f.close()
        f = open(self.file, "rb")
        raw_result = f.read()
        f.close()

        try:
            self.assertEqual(data, result)
            self.assertEqual(data.encode('utf-8'), raw_result)
        finally:
            os.remove(self.file)


if __name__ == "__main__":
    unittest.main()