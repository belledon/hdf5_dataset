# hdf5_dataset
Converts path structure to hdf5 recursively

Version 0.1.0


## Supported file types:

Relies on Numpy's `np.void` array to preserve binary data.

## Requirements:
- python 3
- h5py
- numpy
- pillow (for example)

## Installation:

Simply run `python3 -m pip install .` from this directory.

## Usage:

### Creating a hdf5 dataset

The general philosophy of this package is structure agnostic.
The example dataset is purely an "example". Feel free to experiment
with other directory structures that suit your projects better.

When you are ready to create a hdf5 dataset, use `h5data-create`,
which was installed as part of this pacakge.

```
usage: h5data-create [-h] [--out OUT] root

Converts directorty tree to hdf5

positional arguments:
  root               Root path

optional arguments:
  -h, --help         show this help message and exit
  --out OUT, -o OUT  Path to save dataset. Default is CWD
```

This package crawls through a path and writes each file's content into an hdf5 dataset by reading the file as binary.
Doing so gives the advantage of not requiring dependencies but defers data
processing when accessing the resulting hdf5 file.

Fortunately, there are simple solutions, such as Python's `io.BytesIO` class which then treats the dataset as a file object. 
This often means that you can convert the raw bytes into a file object that can
then be passed to your favorite data type (i.e. `numpy.ndarray`)

Below is a simple dummy script deffering file formatting until access.

```python
import h5py
import soundfile as sf
from io import BytesIO

# here 'data.hdf5' was created from h5data-create
with h5py.File('data.hdf5') as f:
    raw = f['arbitrary/path/to/audio'].value
    byte_file = BytesIO(raw)
    (audio, sample_rate) = sf.read(byte_file)
```

See [examples/simple_dataset.py](examples/simple_dataset.py) for a case for `numpy`.

### Dataset interface

The general interface for extracting trial data is defined in [h5data.dataset.HDF5Dataset](h5data/dataset.py)
