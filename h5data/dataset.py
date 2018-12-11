import h5py
import numpy as np
from abc import ABC, abstractmethod


class HDF5Dataset(ABC):

    '''An interface class for hdf5 dataset interfacing

    Attributes:
       source (str)
       root (str)
       trials (dict)


    Methods:
        __len__ : Returns the number of trials found
        __getitem__
        get_example : Given an integer, returns a tuple containting the input
            and the ground truth for that trial
        process_trial
    '''

    @property
    @abstractmethod
    def source(self):
        """The path to the hdf5 file."""
        pass

    @property
    @abstractmethod
    def root(self):
        """A subpath within the hdf5 file."""

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def trials(self):
        """Returns a dictionary of paths per part in the trial
        Returns:
            parts (dict) : paths to data organized with keys corresponding to
                `self.trail_funcs`.
        '''
        """
        pass

    @property
    @abstractmethod
    def trial_funcs(self):
        """A dictionary containing functions that process raw trial components

        Each key corresponds to an element in the trial, with the corresponding
        value used to process raw byte information in `get_trial`.

        example:
            { 'image': foo,
              'label': bar
            }
        """
        pass

    @abstractmethod
    def process_trial(self):
        ''' Configures the parts of a trial into a tuple (input, target).

        For example, if a trial contains only two components, such as an image
        and a label, then this function can simple return (image, label).

        However, this function can return an arbitrary tuple as long as the
        outermost layer is a (input, target) tuple.

        examples:

        ((a, b, c), (d, e)) # where (a,b,c) are different inputs for a model
                            # and (d,e) are targets for a mutli-task network
        '''
        pass

    def get_trial(self, i, f):
        """Returns the trial corresponding to the given index.

        Obtains the raw trial data and passes those components to
        `process_trial`.

        Arguments:
            index (int): Index of trial
            f (h5py.File, h5py.Group, optional): A hdf5 object that
            stores the raw trial data.
        Returns:
            A tuple of the form (input, target)
        """

        trial_parts  = self.trials(i, f)
        trial_funcs = self.trial_funcs
        parts = {}

        for key in trial_parts:
            if key in trial_funcs:
                path = trial_parts[key]
                p_func = trial_funcs[key]
                try:
                    raw = f[path].value
                except:
                    msg = '{} not found in trial {}'.format(path, i)
                    raise KeyError(msg)
                part = p_func(raw)
            else:
                part = trial_parts[key]

            parts[key] = part

        return self.process_trial(parts)

    def __getitem__(self, idx):
        """Returns items in the dataset
        """
        with h5py.File(self.source, 'r') as f:
            root = f[self.root]
            if isinstance(idx, slice):
                return [self.get_trial(ii, root)
                    for ii in range(*idx.indices(len(self)))]
            elif isinstance(idx, list) or isinstance(idx, np.ndarray):
                return [self.get_trial(i, root) for i in idx]
            else:
                if idx > len(self) - 1:
                    raise IndexError("Requested trial {0:d} for dataset of length {1:d}".format(
                    idx, len(self)))
                elif idx < 0:
                    raise IndexError("Requested trial with negative index")
                else:
                    return self.get_trial(idx, root)
