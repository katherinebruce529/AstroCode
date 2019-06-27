#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 10:01:17 2019

@author: katiebruce
"""

from astropy import time, coordinates as coord, units as u
import pandas as pd

df = input("Enter the CVS path and name: ")
df = pd.read_csv(df, index_col=False) 
col = input('Enter the JD column name: ')

choice = eval(input("Enter 1 for HJD or 2 for BJD. "))
hourangle = input("Enter the hour angle: ")
deg = input("Enter the degrees: ")
ip_peg = coord.SkyCoord(hourangle, deg, unit =(u.hourangle,u.deg), frame = 'icrs')

print("Run coord.EarthLocation.get_site_names() to see a list of locations")
location = input("Enter the location: ")
earthlocation = coord.EarthLocation.of_site(location)
date = []
for n in range(len(df)):
    var = df[col][n]
    times = time.Time([var], format='jd', scale='utc',location=earthlocation)
    if choice == 1: 
        ltt_helio= times.light_travel_time(ip_peg, 'heliocentric')
        time_heliocenter = times.utc + ltt_helio
        x = time_heliocenter.jd
        x = float(x)
        date.append(x)
    # FOR BJD
    if choice == 2:
        ltt_bary = times.light_travel_time(ip_peg)
        time_barycenter = times.tdb + ltt_bary
        x = time_barycenter.jd
        x = float(x)
        date.append(x)
date = pd.DataFrame(date)
if choice == 1: 
    date.columns = ['HJD']
if choice == 2:
    date.columns = ['BJD']
del df[col]
df = df.join(date)
outfile = input("Enter the output path and name: ")
df.to_csv(outfile, index=False)