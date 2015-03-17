The `okeanidanalysis` package is a `python` package to help you plot and
analyze data from a long-range AUV.

It is being developed and tested to work with Python 3.4.2, but should mostly
work with other recent versions.

Installing non-python dependencies
----------------------------------

If you want to use one of the interactive backends for matplotlib,
it seems easiest to use your distro package manager right now.
To support both agg and cairo in GTK:
```Shell
sudo pacman -S agg cairo pygtk python2-pyqt4
```

If you want to use the Qt backend, you need to get PyQt running on your machine
(see [this post](http://bit.ly/1qLTtcz) for tips).
**TODO** distill instructions into a recipe in this repository,
and offer alternatives (GTK, wx, etc.)

Then install the non-python dependencies for `scipy`, `matplotlib`, etc:
```Shell
sudo pacman -S lapack blas libpng freetype2 libxml2 libxslt hdf netcdf geos
```
```Shell
sudo pacman -S python2 python2-pip
```

*TODO* Update for python3

Making a venv
-------------

Installing python dependencies via pip
--------------------------------------
```Shell
pip install numpy scipy h5py netCDF4 pyproj pyparsing tornado python-dateutil pytz matplotlib ipython
pip install https://github.com/matplotlib/basemap/archive/v1.0.6rel.tar.gz#egg=basemap
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
