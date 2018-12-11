import io
import os
from copy import deepcopy
from pprint import pprint

import h5py
import numpy as np
from h5data import dataset
from PIL import Image, ImageOps


def get_image(raw):
    """Converts a raw bytestring to a PIL.Image"""
    s = raw.tostring()
    f = io.BytesIO(s)
    image = Image.open(f)
    image = image.resize((227, 227))
    return image

def get_text(raw):
    """Converts a raw bytestring to an ASCII string"""
    ba = bytearray(raw)
    s = ba.decode('ascii')
    return s


class SimpleDataset(dataset.HDF5Dataset):

    """A simple implementation of `h5data.dataset.HDF5Dataset`"""

    def __init__(self, source):

        self.source = source

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, path):
        if not os.path.isfile(path):
            raise ValueError('Source does not exist')

        # WARNING
        # This is a bad idea if the dataset is really large
        with h5py.File(path, 'r') as f:
            root = f[self.root]
            self.size = len(root)
        self._source = path

    @property
    def root(self):
        return '/trials'

    def __len__(self):
        return self.size

    def trials(self, index, handle):
        parts = {}
        path = '{0:d}'.format(index)
        parts['image'] = os.path.join(path, 'image.png')
        parts['label'] = os.path.join(path, 'text')
        # keys that are not in `trial_funcs` are carried over in `get_trial`
        parts['flip'] = np.random.sample() < 0.5
        parts['gray'] = np.random.sample() < 0.3
        pprint(parts)
        return parts

    @property
    def trial_funcs(self):
        d = {
            # part of input
            'image' : get_image,
            # target
            'label' : get_text,
        }
        return d

    def process_trial(self, parts):

        pprint(parts)
        image = parts['image']
        if parts['gray']:
            image = image.convert('L').convert('RGB')
        if parts['flip']:
            image = ImageOps.mirror(image)

        image = np.asarray(image)[:, :, :3]
        image = np.moveaxis(image, 2, 0)

        return (image, parts['label'])


def main():

    path = 'dataset.hdf5'
    ds = SimpleDataset(path)
    for t_i in range(len(ds)):
        i, l = ds[t_i]
        print(i.shape)
        print(l)

    img = np.moveaxis(i, 0, 2).astype(np.uint8)
    img = Image.fromarray(img)
    img.save('test_id.png')

if __name__ == '__main__':
    main()
