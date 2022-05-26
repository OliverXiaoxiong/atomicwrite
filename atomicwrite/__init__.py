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
            content = kwargs['content']
            file = kwargs['file']
            mode = kwargs['mode']
            fd = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(file))

            try:
                # preserve file metadata if it already exists
                if os.path.exists(file):
                    deep_copy(file, fd.name)
                if kwargs.get('encoding', None):
                    f = codecs.open(fd.name, mode, kwargs['encoding'])
                else:
                    f = open(fd.name, mode)
                f.write(content)
                f.flush()
                os.fsync(f.fileno())
                f.close()

                os.replace(fd.name, file)
            finally:
                if os.path.exists(fd.name):
                    try:
                        os.unlink(fd.name)
                    except:
                        pass
        try:
            temp_write(*args, **kwargs)
            return func(*args, **kwargs)
        except:
            raise SystemExit("Atomic writing failed.")

    return wrappers

