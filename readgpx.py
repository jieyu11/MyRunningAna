#!/usr/bin/env python

import gpxpy
import matplotlib.pyplot as plt
# import datetime
# from geopy import distance
# from math import sqrt, floor
import numpy as np
import pandas as pd
# import plotly.plotly as py
# import plotly.graph_objs as go
# import haversine
from mpl_toolkits.basemap import Basemap


gpx_file = open('data/533829103.gpx', 'r')
gpx = gpxpy.parse(gpx_file)
data = gpx.tracks[0].segments[0].points
df = pd.DataFrame(columns=['lon', 'lat', 'alt', 'time'])
ln = []
lt = []
for point in data:
    df = df.append({'lon': point.longitude,
                    'lat': point.latitude,
                    'alt': point.elevation,
                    'time': point.time},
                   ignore_index=True)
    ln.append(point.longitude)
    lt.append(point.latitude)
#    print("long:", point.longitude,
#          "lati:", point.latitude,
#          "alti:", point.elevation)

print("longitude: (min, max)", np.min(ln), ",", np.max(ln))
print("latitude: (min, max)", np.min(lt), ",", np.max(lt))

m = Basemap(resolution='c',  # c, l, i, h, f or None
            projection='merc',
            lon_0=-93.625, lat_0=42.035,
            llcrnrlon=-93.7, llcrnrlat=42.02,
            urcrnrlon=-93.55, urcrnrlat=42.05)
m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=1500, verbose=True)

plt.plot(df['lon'], df['lat'])
plt.show()
