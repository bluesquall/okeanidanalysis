#!/usr/bin/env python
import os
import urllib2
import matplotlib.pyplot as plt
import okeanidanalysis as oa

# set up the map
mbm = oa.maps.MontereyBay(resolution='i')
mbm.drawdefault()

kml_path = os.path.join('..','..','data','shore','20140608T072137','shore.kml')
print kml_path

# pass the path to the kml
mbm.draw_kml(kml_path) 

# pass an open python file object
with open(kml_path) as f: mbm.draw_kml(f)

# pass a string containing all of the kml
with open(kml_path) as f: 
    kml_string = f.read()
    mbm.draw_kml(kml_string, fromstring=True)

# pull it from the internet and plot it
url = 'http://aosn.mbari.org/TethysDash/data/daphne/realtime/sbdlogs/2014/201406/20140608T072137/shore.kml'
mbm.draw_kml(urllib2.urlopen(url))

plt.show()
