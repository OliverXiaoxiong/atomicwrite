import os
import shutil
import stat
import codecs
import tempfile
from functools import wraps


def atomic_write(function):
    ''' 
    An decorator for performing atomic writes. Usage:
    
        @atomic_write
        def my_writer(content, file, mode='wb', encoding=None):
            pass
    '''
    
    @wraps(function)
    def wrappers(*args, **kwargs):
        
        def _copy(source: str, target: str):
            
            shutil.copy2(source, target)
            st = os.stat(source)
            os.chown(target, st[stat.ST_UID], st[stat.ST_GID])
        
        
        def _write(*args, **kwargs):
            
            content = kwargs.get('content', '')
            file = kwargs.get('file', '')
            mode = kwargs.get('mode', None)
            encoding = kwargs.get('encoding', None)
            
            # crreate temproary file in the same directory
            fd = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file))

            kwargs['file'] = fd.name
            
            try:
               
                if os.path.exists(file):
                    _copy(file, fd.name)  # keep the metadata if it exists
                if encoding:
                    f = codecs.open(fd.name, mode, encoding) # using codecs open for encoding method
                else:
                    f = open(fd.name, mode)
                f.write(content)
                f.flush()
                os.fsync(f.fileno()) # make sure file contents is written to the temporary file
                f.close()

                os.replace(fd.name, file) # replace file 
            finally:
                if os.path.exists(fd.name):
                    try:
                        os.unlink(fd.name) # remove temporary file
                    except:
                        pass
                    
        try:
            _write(*args, **kwargs)
            return function(*args, **kwargs)
        except:
            pass

    return wrappers

