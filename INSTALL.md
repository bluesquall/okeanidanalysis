The `okeanidanalysis` package is a `python` package to help you plot and
analyze data from a long-range AUV.

It is being developed and tested to work with Python 3.4.2, but should mostly
work with other recent versions.

Installing
----------
If you already have the dependencies, you should install using
[`pip`](http://pip.readthedocs.org), and I recommend you consider a
[`virtual environment`](https://docs.python.org/3/library/venv.html).
```Shell
pip install -e ~/repos/okeanidanalysis
```
or:
```Shell
pip install git+git://github.com/bluesquall/okeanidanalysis.git#egg=okeanidanalysis
```
**TODO** make sure the one above works on a test machine and the pip requirements file is found & used automatically.

Dependencies
------------
The python package requirements are listed in a `pip`-compatible requirements
file: `requirements.txt`.

The major requirements can be installed using the standard approach for your
operating system. For the `python` dependencies, we recommend using `pip`
because it gives more flexible control over python packages, and also allows
you to install a specific revision directly from a version control system.

You will need:

* numpy

* scipy

* matplotlib

  * libpng

  * libfreetype

  * pyparsing

  * tornado

  * python-dateutil

* pytz

* basemap (a matplotlib toolkit for plotting maps and map projections)

* h5py

* lxml

  * libxml2-dev

  * libxslt1-dev

* pykml

* argparse (for some of the example scripts)

You should consider using `pip` and `venv` to install appropriate versions of
all the python dependencies locally without touching the system default
versions. This approach is particularly useful when you are working on a
machine where you don't have administrator privileges, or don't want to
exercise those privileges.

### Installing dependencies via `pip` or from source

If you decide to install dependencies like `numpy`, `scipy`, and `matplotlib`
from source (i.e., instead of using `apt-get`, `brew`, `pacman`, or `yum`),
then you will need to have some other non-python packages installed.

#### numpy
I believe this should install just fine without any external dependencies, but
it will use things like LAPACK if it finds them. (Come back to check on this.)

#### scipy

* lapack

* blas

* atlas

#### matplotlib

You may not _need_ these, but you will probably _want_ them.

* libpng

* freetype

Newer versions of `matplotlib` also include some use of `six` and `tornado`
(follow up on that).

Depending on the backend you plan to use, you may want to install a toolkit and
its python bindings with the package manager for your distro. (PyQt4 doesn't
install in quite the way `pip` expects, so `pip install PyQt4` won't work.)

#### basemap

I believe the basemap distribution includes a copy of libgeos, just in case,
but you probably want to install the one for your system.

* geos

#### pykml and lxml

Before installing lxml in ubuntu, you will need to install:

  * libxml2-dev

  * libxslt1-dev

Afterward, you can install `lxml` and `pykml` via `pip`.


Platform-specific installation instructions
-------------------------------------------

Please refer to `INSTALL.<platform>.md` in the root directory of the repo.
