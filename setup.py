import setuptools

with open("README.rst", "r") as fh:
   long_description = fh.read()

setuptools.setup(
    name="amendment-back-up",
    version="0.1.5",
    author="Yu Sun",
    author_email="sunyu0410@gmail.com",
    description="Incremental backup",
    long_description=long_description,
    # long_description_content_type="text/markdown",
    url="https://github.com/sunyu0410/AmendmentBackUp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: System :: Archiving :: Backup",
    ],
)
