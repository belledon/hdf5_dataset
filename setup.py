import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="h5data",
    version="0.0.1",
    author="Mario Belledonne",
    author_email="mbelledonne@gmail.com",
    description="Tools to create and access hdf5 datasets for ML.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages = ['h5data'],
    entry_points = {
        'console_scripts' : [
            'h5data-create = h5data.hdf5:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
