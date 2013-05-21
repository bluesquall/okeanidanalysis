#!/usr/bin/env python

import numpy as np
import okeanidanalysis as oa

filenameA = '../../data/shore/20130314T133105/shore.mat'
filenameB = '../../data/shore/20130319T085014/shore.mat'

A = oa.logs.OkeanidLog(filenameA,'r')
B = oa.logs.OkeanidLog(filenameB,'r')

signal = 'mass_concentration_of_chlorophyll_in_sea_water'
TA = np.diff(A['/'.join((signal,'time'))][[-1,0]].ravel())[0] * 24 # timespan [hours]
TB = np.diff(B['/'.join((signal,'time'))][[-1,0]].ravel())[0] * 24 # timespan [hours]

NA = len(A['/'.join((signal,'value'))][:].ravel())
NB = len(B['/'.join((signal,'value'))][:].ravel())

print
print 'signal: ', signal
print
print filenameA
print 'timespan: ', TA, 'hours;', 'N:', NA, 'counts;', NA/TA, 'counts/hour'
print filenameB
print 'timespan: ', TB, 'hours;', 'N:', NB, 'counts;', NB/TB, 'counts/hour'

