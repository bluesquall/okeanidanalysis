The `okeanidanalysis` package is a `python` package to help you plot and
analyze data from a long-range AUV.

It is being developed and tested to work with Python 3.4.2, but should mostly
work with other recent versions.

Installing non-python dependencies
----------------------------------

*TODO* Recompile list and add it here.

*TODO* Check interactive backends.

Making a venv
-------------

Installing python dependencies via pip
--------------------------------------
In your python (2.7 or 3.x) virtualenv:
```Shell
pip install -U numpy scipy  h5py netCDF4 python-dateutil six tornado pyparsing pytz lxml pykml matplotlib basemap ipython
```

The current (2014-10-10) version of freetype2 on CentOS 6.5 is 2.3.11, but
matplotlib wants 2.4. According to [this StackOverflow post](http://stackoverflow.com/questions/25634689/installing-matplotlib-on-centos-6-5),
matplotlib should be fine with freetype2-2.3.11, but your mileage may vary.

If you want to use freetype 2.3:
```Shell
pip install -U numpy scipy  h5py netCDF4 python-dateutil six tornado pyparsing pytz
pip install --download /tmp matplotlib
cd /tmp && tar -xvf matplotlib-1.4.0.tar.gz
vim matplotlib-1.4.0/setupext.py
  :945
  :s/2\.4/2\.3/
  :wq
tar -czvf matplotlib-1.4.0.tar.gz matplotlib-1.4.0
pip install --verbose matplotlib-1.4.0.tar.gz
pip install https://github.com/matplotlib/basemap/archive/v1.0.7rel.tar.gz#egg=basemap
pip install ipython
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
