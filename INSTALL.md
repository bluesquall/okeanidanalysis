The `okeanidanalysis` package is a `python` package to help you plot and analyze data from a long-range AUV.

It has been developed primarily using Python 2.7.3, but should mostly work with other versions.

Installing
----------
If you already have the dependencies, you can install directly using `setuptools`:

foo@bar okeanidanalysis$ sudo python setup.py install

Personally, I prefer using `pip`:

foo@bar ~$ sudo pip install -e ~/repos/okeanidanalysis

or:

foo@bar ~$ sudo pip install git+git://github.com/bluesquall/okeanidanalysis.git#egg=okeanidanalysis

**TODO** make sure the one above works on a test machine and the pip requirements file is found & used automatically.

Dependencies
------------
The python package requirements are listed in a `pip`-compatible requirements file: `requirements.txt`.

The major requirements can be installed using the standard approach for your OS, or using `pip`. I personally prefer `pip` because it gives more flexible control over python packages, and even allows you to install a specific revision directly from a version control system.

You will need:

* numpy

* scipy

* matplotlib
  
  * libpng
  
  * libfreetype

  * pyparsing

  * tornado

  * python-dateutil

* basemap (a matplotlib toolkit for plotting maps and map projections)

* h5py

* lxml

  * libxml2-dev 
  
  * libxslt1-dev

* pykml

* argparse (for some of the example scripts)

You may also want to consider using `pip` and `virtualenv` to install appropriate versions of all the python dependencies locally without touching the system default versions. This approach is particularly useful when you are working on a machine where you don't have administrator privileges, or don't want to exercise those privileges.

### Installing dependencies via `pip` or from source

If you decide to install dependencies like `numpy`, `scipy`, and `matplotlib` from source (e.g., instead of using `apt-get` or `yum`), then you will need to have some other non-python packages installed.

#### numpy
I believe this should install just fine without any external dependencies, but it will use things like LAPACK if it finds them. (Come back to check on this.)

#### scipy

* lapack

* blas

* atlas

#### matplotlib

You may not _need_ these, but you will probably _want_ them.

* libpng

* freetype

Newer versions of `matplotlib` also include some use of `six` and `tornado` (follow up on that).

#### basemap

I believe the basemap distribution includes a copy of libgeos, just in case, but you probably want to install the one for your system.

* geos

#### pykml and lxml

Before installing lxml in ubuntu, you will need to install:

  * libxml2-dev 
  
  * libxslt1-dev

Afterward, you can install `lxml` and `pykml` via `pip`.

### Table of non-python dependencies and suggested packages:
**TODO** make this for Ubuntu 12.04 and CentOS 6, at least.

example shell script for pip install
------------------------------------
For Ubuntu 12.04:
```Shell
sudo apt-get install libpng12-dev libfreetype6-dev libxml2-dev libxslt1-dev
sudo pip install numpy
sudo pip install scipy
sudo pip install pyparsing tornado python-dateutil
sudo pip install matplotlib
sudo pip install h5py
sudo pip install ipython
sudo pip install pyproj
sudo pip install https://github.com/matplotlib/basemap/archive/v1.0.6rel.tar.gz#egg=basemap
sudo pip install lxml pykml
```
