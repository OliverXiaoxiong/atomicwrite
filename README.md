# Atomic Writing for Python
[![Build Status](https://app.travis-ci.com/OliverXiaoxiong/atomicwrite.svg?branch=master)](https://app.travis-ci.com/OliverXiaoxiong/atomicwrite)

A simple implementation of decorator  to guarantee that the data is not partially written to the file by writing to a temporary file that gets renamed and deleted after writing.

**Usage**:
```Python
from atomicwrite import atomic_write

@atomic_write
my_writer(content, file, mode='wb'):
    pass
```

**Run a demo of decorator on a parquet file**
```Python
python parquet_demo.py
```

**Run unit test**
```Python
python test_atomicwrite.py
```