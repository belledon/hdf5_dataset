import h5py 
import json
import numpy as np
import fileFuncs as ff
from PIL import Image
import argparse

loaders = {".npy" : np.load, 
		".png" : Image.open, 
		".jpeg" : Image.open, 
		".json" : json.open, }
	


class Folder:
	
	def __init__(self, source, f):

		group = f.create_group(ff.fileBase(source))

		for file in ff.find(source, "."):
			try:
				f_obj = File(file, ff.fileExt(file))
				f_obj(group)

			except ValueError e:
				print("File {} could not be added because of:\n {}".format(
					file, e))

		for folder in ff.findDir(source):
			Folder(folder, group)

		self.group = group


class File:

	def __init__(self, source, ext, loaders = loaders):

		self.loaders = loaders
		self.source = source
		self.loaded = load_data(ext)

	def __call__(self, group):

		source_id = ff.fileName(self.source)
		group.create_dataset(source_id, self.loaded)



	def load_data(self, ext):
		if ext not in self.loaders.keys():
			raise ValueError("Ext {} not supported ({})".format(
				ext, self.loaders.keys()))

		loader = self.loaders[ext]
		with loader(file) as d:
			loaded = np.asarray(d)

		return loaded