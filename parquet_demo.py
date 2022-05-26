import os
import pandas as pd

from atomicwrite import atomic_write

@atomic_write
def my_writer(content, file, mode='wb', encoding=None):
    pass


if __name__ == "__main__":
    parquet_file = './userdata1.parquet'
    save_file = './res.parquet'
    
    f = open(parquet_file, 'rb')
    data = f.read()
    f.close()
    my_writer(content=data, file=save_file, mode='wb')
    
    df = pd.read_parquet(parquet_file, engine='pyarrow')
    df2 = pd.read_parquet(save_file, engine='pyarrow')
    
    try:
        assert df.equals(df2), 'Failed'
    finally:
        os.remove(save_file)