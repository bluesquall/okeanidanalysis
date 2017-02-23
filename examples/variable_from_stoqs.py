#!/usr/bin/env python

import matplotlib.pyplot as plt

import postgresql

dbargs = dict(  user='everyone', 
                password='guest', 
                host='kraken.shore.mbari.org', 
#                database='canon/stoqs_canon_may2015_lrauv',
                database='stoqs_canon_may2015_lrauv',
             )

dbaddr = 'pq://{user}:{password}@{host}/{database}'.format(**dbargs)
squery = '''
SELECT stoqs_measuredparameter.parameter_id,
       stoqs_parameter.name,
       stoqs_parameter.standard_name,
       stoqs_measurement.depth,
       stoqs_measurement.geom,
       stoqs_instantpoint.timevalue,
       stoqs_activity.name,
       stoqs_platform.name,
       stoqs_measuredparameter.datavalue,
       stoqs_parameter.units
FROM stoqs_measuredparameter
     INNER JOIN stoqs_measurement ON (stoqs_measuredparameter.measurement_id = stoqs_measurement.id)
     INNER JOIN stoqs_instantpoint ON (stoqs_measurement.instantpoint_id = stoqs_instantpoint.id)
     INNER JOIN stoqs_parameter ON (stoqs_measuredparameter.parameter_id = stoqs_parameter.id)
     INNER JOIN stoqs_activity ON (stoqs_instantpoint.activity_id = stoqs_activity.id)
     INNER JOIN stoqs_platform ON (stoqs_activity.platform_id = stoqs_platform.id)
WHERE (stoqs_instantpoint.timevalue <= '2015-05-30 04:31:20'
      AND stoqs_instantpoint.timevalue >= '2015-05-27 09:02:29'
      AND stoqs_parameter.name IN ('bin_median_mass_concentration_of_chlorophyll_in_sea_water')
      AND stoqs_measurement.depth >= -9.49
      AND stoqs_platform.name IN ('daphne')
      AND stoqs_measurement.depth <= 75.4
      AND stoqs_measuredparameter.parameter_id = 9)
ORDER BY stoqs_activity.name ASC, stoqs_instantpoint.timevalue ASC
'''

sdb = postgresql.open(dbaddr)
res = sdb.query(squery)
print(res)

