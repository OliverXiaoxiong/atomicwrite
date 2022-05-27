import os
import shutil
import stat
import codecs
import tempfile
from functools import wraps


def atomic_write(func):
    @wraps(func)
    def wrappers(*args, **kwargs):
        def deep_copy(source, target):
            
            shutil.copy2(source, target)
            st = os.stat(source)
            os.chown(target, st[stat.ST_UID], st[stat.ST_GID])

        def temp_write(*args, **kwargs):
            content = kwargs.get('content', '')
            file = kwargs.get('file', None)
            mode = kwargs.get('mode', None)
            
            # crreate temproary file in the same directory
            fd = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file))

            try:
               
                if os.path.exists(file):
                    deep_copy(file, fd.name)  # keep the metadata if it exists
                if kwargs.get('encoding', None):
                    f = codecs.open(fd.name, mode, kwargs['encoding']) # using codecs open for encoding method
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
            temp_write(*args, **kwargs)
            return func(*args, **kwargs)
        except:
            raise SystemExit("Atomic writing failed.")

    return wrappers

