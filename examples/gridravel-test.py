#!/usr/bin/env python
"""
gridravel-test
==============

Confirm that oa.lib.gridravel and oa.lib.gridunravel function as inverses.

"""
import datetime
import numpy as np
import matplotlib.pyplot as plt
import okeanidanalysis as oa

oma = oa.currents.OpenBoundaryModalAnalysis()
dto = datetime.datetime(2012,10,01,0,0)
oma.open_datetime_url(dto)
dlon, dlat, du = oa.lib.gridravel(oma.longitude, oma.latitude, oma.u)
ustar = oa.lib.gridunravel(dlon, dlat, du)

idx = ~np.isnan(oma.u)
print 'np.allclose(...)', np.allclose(oma.u[idx], ustar[idx])

glon, glat = np.meshgrid(oma.longitude, oma.latitude)
fig = plt.figure(100)
m = oa.maps.MontereyBay(resolution='i')
m.drawdefault() 
m.contourf(glon, glat, oma.u - ustar, 50, latlon=True)
m.drawgrid()
plt.title('ravel-unravel test')
plt.colorbar()

plt.show()
