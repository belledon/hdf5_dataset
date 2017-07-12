import argparse
import h5py
import hdf5

def main():
	parser = argparse.ArgumentParser(description = "Converts directorty tree to hdf5")

	parser.add_argument("root", type =str, 
		help = "Root path")

	parser.add_argument("--out", "-o", type = str, default = os.getcwd(),
		help = "Path to save dataset. Default is CWD")


	args = parser.parse_args()

	print("Supported files are {}".format(hdf5.loaders.keys()))

	if not ff.isDir(args.root):
		raise ValueError("{} is not a valid path".format(args.root))

	ff.ensureDir(args.out)
	root_base = ff.fileBase(args.root)
	out = ff.join(args.out, "{}.hdf5".format(root_base))

	print("Save destination: {}".format(out))
	print("Beginning HDF5 conversion")
	with h5py.File(out, "w") as f:
		hdf5.Folder(args.root, f)

	print("HDF5 conversion complete")