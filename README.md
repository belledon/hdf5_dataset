# hdf5_dataset
Converts path structure to hdf5 recursively

Version 0.2.0


## Supported file types:

Relies on Numpy's `np.void` array to preserve binary data.

## Requirements:
- python 3
- h5py
- numpy

## Usage:

```
usage: hdf5.py [-h] [--out OUT] root

Converts directory tree to hdf5

positional arguments:
  root               Root path

optional arguments:
  -h, --help         show this help message and exit
  --out OUT, -o OUT  Path to save dataset. Default is CWD
```

This package crawls through a path and writes each file's content into an hdf5 dataset by reading the file as binary.
Doing so gives the advantage of not requiring dependencies but defers data processing when accessing the resulting hdf5 file.

Fortunately, there are simple solutions, such as Python's `io.BytesIO` class which then treats the dataset as a file object. 

Below is a simple dummy script deffering file formatting until access.

```python
import h5py
import soundfile as sf
from io import BytesIO

# here 'data.hdf5' was created from this hdf5_dataset.py
with h5py.File('data.hdf5') as f:
    raw = f['arbitrary/path/to/audio'].value
    byte_file = BytesIO(raw)
    (audio, sample_rate) = sf.read(byte_file)
```
