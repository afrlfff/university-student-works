import numpy as np
import pandas as pd
import os

# ==============================================================================

def read_data(file_path: str, max_rows: int | None = None) -> np.ndarray:
    return pd.read_csv(
        file_path, header=None, sep='|', decimal=',',
        nrows=max_rows, engine='c', usecols=[0]
    ).to_numpy(dtype=np.float64).ravel()

# ==============================================================================

def count_rows(file_path: str) -> int:
    if os.path.getsize(file_path) == 0:
        return 0
    
    n = 0
    with open(file_path, 'rb') as f:
        while chunk := f.read(1 << 20):
            n += chunk.count(b'\n')

    return n + (chunk[-1:] != b'\n')

# ==============================================================================

def read_data_writable(path: str, max_rows: int | None = None, n_chunk_rows: int = 10000) -> np.ndarray:
    if max_rows is None:
        max_rows = count_rows(path)
    arr = np.empty(max_rows, dtype=np.float64)

    idx = 0
    for df in pd.read_csv(path, chunksize=n_chunk_rows, nrows=max_rows, header=None, decimal=',', engine='c', usecols=[0]):
        chunk = df.iloc[:, 0].to_numpy()
        arr[idx:idx+len(chunk)] = chunk
        idx += len(chunk)
    
    return arr

# ==============================================================================