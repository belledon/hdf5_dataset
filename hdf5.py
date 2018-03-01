import h5py 
import json
import numpy as np
import fileFuncs.ff as ff
from PIL import Image
import argparse
import os
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
def np_load(file):
	yield np.load(file)

@contextmanager
def json_load(file):
	yield bytearray(open(file).read(), 'ascii')

loaders = {".npy" : np_load, 
		".png" : Image.open, 
		".jpeg" : Image.open, 
		".json" : json_load , }


class Folder:
	
	def __init__(self, source, f, root = False):
		if root:
			group = f
		else:
			group = f.create_group(ff.fileBase(source))

		for file in ff.find(source, "*.*"):
			try:
				f_obj = File(file, ff.fileExt(file))
				f_obj(group)

			except ValueError as e:
				print("File {} could not be added because of:\n {}".format(
					file, e))

		for folder in ff.findDir(source):
			Folder(folder, group)

		self.group = group


class File:

	def __init__(self, source, ext, loaders = loaders):

		self.loaders = loaders
		self.source = source
		self.loaded = self.load_data(ext)

	def __call__(self, group):

		source_id = ff.fileName(self.source)
		group.create_dataset(source_id, data=self.loaded)



	def load_data(self, ext):
		if ext not in self.loaders.keys():
			raise ValueError("Ext {} not supported ({})".format(
				ext, self.loaders.keys()))

		loader = self.loaders[ext]
		# print(loader.__exit__)
		with loader(self.source) as d:
			loaded = np.asarray(d)

		return loaded

def main():
	parser = argparse.ArgumentParser(description = "Converts directorty tree to hdf5")

	parser.add_argument("root", type =str, 
		help = "Root path")

	parser.add_argument("--out", "-o", type = str, default = os.getcwd(),
		help = "Path to save dataset. Default is CWD")


	args = parser.parse_args()

	print("Supported files are {}".format(loaders.keys()))

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
