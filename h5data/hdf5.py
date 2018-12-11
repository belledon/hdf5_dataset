""" HDF5 Creator.

This script converts an arbitrary directory to an hdf5 file.

Classes:

    Folder
    File

"""

import os
import h5py
import argparse
import numpy as np

class Folder:

    """Group analog of hdf5 structure.

    Represents a directory as a hdf5 group.
    The source directory's name is the name of the group.

    """

    def __init__(self, origin, handle):
        """ Creates an instance of `Folder`

        Parameters:
            origin (str): The directory to search.
            handle (h5py.File): The file object associate with the dataset.
        """
        if not isinstance(handle, h5py.File):
            raise TypeError('handle must be `h5py.File`')

        root = os.path.basename(handle.filename)
        root = os.path.splitext(root)[0]
        bridge = origin.split(root)[-1]

        contents = os.listdir(origin)

        for element in contents:
            path = os.path.join(origin, element)
            if os.path.isfile(path):
                try:
                    f_obj = File(path, handle)

                except ValueError as e:
                    print("File {} could not be added because of:\n {}".format(
                        path, e))
            elif os.path.isdir(path):
                g_path = os.path.join(handle.name, bridge, element)
                group = handle.create_group(g_path)
                Folder(path, handle)


class File:

    """Dataset analog of hdf5 structure.

    Consists of a dataset containing the source files contents as bytes.
    The name of the source file is the name of the dataset.

    """

    def __init__(self, source, handle):
        """ Creates an instance of `File`

        Parameters:
            source (str): The file to load.
            handle (h5py.File): The file object associate with the dataset.
        """
        root = os.path.basename(handle.filename)
        root = os.path.splitext(root)[0]
        bridge = source.split(root)[-1]
        path = os.path.join(handle.name, bridge)
        with open(source, 'rb') as d:
            raw = d.read()
            data = np.void(raw)
        handle.create_dataset(path, data=data)


def main():
    parser = argparse.ArgumentParser(
        description = "Converts directorty tree to hdf5"
    )

    parser.add_argument("root", type =str, help = "Root path")

    parser.add_argument("--out", "-o", type = str, default = os.getcwd(),
                        help = "Path to save dataset. Default is CWD")
    args = parser.parse_args()


    if not os.path.isdir(args.root):
        raise ValueError("{} is not a valid path".format(args.root))

    out = os.path.join(args.out, os.path.basename(args.root) + '.hdf5')
    if os.path.exists(out):
        raise ValueError('{} already exists'.format(out))

    print("Save destination: {}".format(out))
    print("Beginning HDF5 conversion")
    with h5py.File(out, "w") as f:
        Folder(args.root, f)

    print("HDF5 conversion complete")

if __name__ == '__main__':
    main()
