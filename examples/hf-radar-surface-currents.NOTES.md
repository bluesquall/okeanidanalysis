I originally tried to do this using `pydap` andt the netCDF subset service for grids... it did not work (pydap returned an issue with an unusable token or something)

url = 'http://hfrnet.ucsd.edu/thredds/ncss/grid/HFRNet/USWC/1km/hourly/RTV?var=u,v&north=37&south=36.5&east=-121.75&west=-122.5&time_start=2012-09-12T12:00:00Z&time_end=2012-09-12T13:00:00Z&accept=application/x-netcdf'

from pydap.client import open_url
data = open_url(url)
Exception: Unable to parse token:


from netCDF4 import Dataset
data = Dataset(url)
RuntimeError: NetCDF: DAP server error
 (and some context message that showed a HTTP 404 not found)

but if you plug that url directly into a browser, it downloads a file called RTV.nc

... eventually, I changed tack and just downloaded to a temp file
ncfile, httpheader = urllib.urlretrieve(url)
data = Dataset(ncfile)
and that works!

Problems with coverage
----------------------
I was originally trying to use the 1km resolution dataset from hfrnet netCDF files, but I couldn't get it to plot.
Then I switched to the cencalcurrents gnome netCDF, and everything seemed to work ok.
Now, looking at (http://www.cencoos.org/sections/conditions/Google_currents/) I see that the 1km resolution dowes not actually cover Monterey Bay -- but the 2km data does.
I'm going to try plotting again with the 2km data, and think about how I should handle data at two different resolutions.


