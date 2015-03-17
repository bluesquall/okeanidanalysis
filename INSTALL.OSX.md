Installing `okeanidanalysis` on Mac OS X
========================================

The `okeanidanalysis` package is a `python` package to help you plot and
analyze data from a long-range AUV.

It is being developed and tested to work with Python 3.4, but should mostly
work with other recent versions.

These installation instructions have been tested on OS X version 10.10.2
(Yosemite), and will hopefully work for you on other recent versions.

Installing `brew`
-----------------

If you are developing or using open-source software on OS X, you really should
be using [homebrew](http://brew.sh/). This is all you need to get started:

```shell
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
brew doctor
```

For more information, [read the docs](https://git.io/brew-docs).

Installing non-python dependencies
----------------------------------

```shell
brew tap homebrew/science
brew update
brew install hdf5 netcdf geos proj python3 gcc freetype
```

... and go get a cup of coffee while `brew` works through all the dependencies
of the dependencies

*NOTE* The `IPython QtConsole` wouldn't work on OSX when we last tried, but the
normal `IPython` terminal console works fine with the OS X backend. (You will
see `Using matplotlib backend: MacOSX`).

Making a venv and activating it
-------------------------------

```shell
pyvenv ~/Virtualenvs/oa
source ~/Virtualenvs/oa/bin/activate
```

Note that you will need to activate your venv any time you open a new terminal
and want to use it.

Installing python dependencies via pip
--------------------------------------

```shell
pip install numpy scipy pyproj matplotlib ipython
pip install h5py netCDF4
```

Get matplotlib-basemap using pip and the external unverified package:
```shell
pip install basemap --allow-external basemap --allow-unverified basemap
```
or via tarball:
```shell
pip install https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz#egg=basemap
```

Installing okeanidanalysis
--------------------------
To install from your local clone of the repository:
```shell
pip install -e /path/to/okeanidanalysis
```
or to install from the master repository on github:
```shell
pip install git+git://github.com/bluesquall/okeanidanalysis.git#egg=okeanidanalysis
```

Checking the installation
-------------------------

```shell
source ~/Virtualenvs/oa/bin/activate
ipython --pylab -i -c "import okeanidanalysis;mbm = okeanidanalysis.maps.MontereyBay(resolution='h');mbm.drawdefault()"
```

You should see a map of the coastline of Monterey Bay, and be left with an
`IPython` terminal session.
