import os
import h5py
import json
import argparse
import numpy as np
import fileFuncs.ff as ff

from PIL import Image
from contextlib import contextmanager

########################################################################
# EXTENDING NEW LOADERS                                                #
########################################################################
# 1. Append the new loader to the loaders dictionary
#
# -- In order to extend loaders that do no support "with as"
# statements, follow the example below:
#
# --- contexmanager adds __enter__ and __exit__ around the generator.
# one only has to yield the data neccessary but more intricate steps
# can occur in the before and after the yield if necessary ---



@contextmanager
def byte_loader(file):
	yield open(file, 'rb').read()


class Folder:

	def __init__(self, source, f, root = False):
		if root:
			group = f
		else:
			group = f.create_group(ff.fileBase(source))

		for file in ff.find(source, "*.*"):
			try:
				f_obj = File(file)
				f_obj(group)

			except ValueError as e:
				print("File {} could not be added because of:\n {}".format(
					file, e))

		for folder in ff.findDir(source):
			Folder(folder, group)

		self.group = group


class File:

	def __init__(self, source):
		self.source = source

	def __call__(self, group):

		source_id = ff.fileName(self.source)
		data = self.load_data()
		group.create_dataset(source_id, data=data)


	def load_data(self):
		with open(self.source, 'rb') as d:
			raw = d.read()
			loaded = np.void(raw)

		return loaded

def main():
	parser = argparse.ArgumentParser(description = "Converts directorty tree to hdf5")

	parser.add_argument("root", type =str,
		help = "Root path")

	parser.add_argument("--out", "-o", type = str, default = os.getcwd(),
		help = "Path to save dataset. Default is CWD")


	args = parser.parse_args()

	# print("Supported files are {}".format(loaders.keys()))

	if not ff.isDir(args.root):
		raise ValueError("{} is not a valid path".format(args.root))

	ff.ensureDir(args.out)
	root_base = ff.fileBase(args.root)
	out = ff.join(args.out, "{}.hdf5".format(root_base))

	print("Save destination: {}".format(out))
	print("Beginning HDF5 conversion")
	with h5py.File(out, "w") as f:
		Folder(args.root, f, root = True)

	print("HDF5 conversion complete")

if __name__ == '__main__':
	main()
