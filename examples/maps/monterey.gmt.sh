#!/bin/bash

## DECLARE YOUR VARIABLES HERE ##
SCALE=18                        # make plot 18 cm across
LATMIN=36.5;    LATMAX=37.      # Latitude range of plots
LONMIN=-122.5;  LONMAX=-121.75  # Longitude range of plots
#################################
GMT gmtset PLOT_DEGREE_FORMAT="D"
#################################
GMT pscoast \
-R$LONMIN/$LONMAX/$LATMIN/$LATMAX -JM$SCALE \
-BWSn0.1g0.05p -Df -Gchocolate -P \
| ps2eps -P -q \
| tee /tmp/monterey-bay-map.eps \
| epstopdf --filter > /tmp/monterey-bay-map.pdf
