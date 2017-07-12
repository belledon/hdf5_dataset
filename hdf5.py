import h5py 
import json
import numpy as np
import fileFuncs.ff as ff
from PIL import Image
import argparse
import os

loaders = {".npy" : np.load, 
		".png" : Image.open, 
		".jpeg" : Image.open, 
		".json" : lambda x: bytearray(x.read(), "ascii") , }
	


class Folder:
	
	def __init__(self, source, f):

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
		with open(self.source) as f:
			d = loader(f)
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
		Folder(args.root, f)

	print("HDF5 conversion complete")

if __name__ == '__main__':
	main()