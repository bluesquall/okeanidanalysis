The `okeanidanalysis` package is a `python` package to help you plot and
analyze data from a long-range AUV.

It is being developed and tested to work with Python 3.4.2, but should mostly
work with other recent versions.

Installing non-python dependencies
----------------------------------

```Shell
sudo apt-get install libpng12-dev libfreetype6-dev libxml2-dev libxslt1-dev
```

*TODO* Check libgeos

*TODO* Remove pykml dependencies

Making a venv
-------------

Installing python dependencies via pip
--------------------------------------

```Shell
pip install numpy scipy h5py netCDF4 pyproj pyparsing tornado python-dateutil pytz matplotlib ipython
pip install https://github.com/matplotlib/basemap/archive/v1.0.6rel.tar.gz#egg=basemap
pip install lxml pykml
```

Installing okeanidanalysis
--------------------------
```Shell
pip install -e ~/repos/okeanidanalysis
```
or:
```Shell
pip install git+git://github.com/bluesquall/okeanidanalysis.git#egg=okeanidanalysis
```
