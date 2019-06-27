#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 10:03:05 2019

@author: katiebruce
"""

from astropy import time, coordinates as coord, units as u

# Enter the coordinates of the object, change the units to the correct units
# The frame defults to the international celestrial reference system
hourangle = input("Enter the hour angle: ")
deg = input("Enter the degrees: ")
ip_peg = coord.SkyCoord(hourangle, deg, unit =(u.hourangle,u.deg), frame = 'icrs')
# This function downloads site information from the astropy data server
# If the site can't be found (lack of internet) it will use a built in list
# ex. 'Cerro Tololo' or 'Kitt Peak' or 'SALT' or 'mdm'
# To get full list:
# coords.EarthLocation.get_site_names()
print("Run coord.EarthLocation.get_site_names() to see a list of locations")
location = input("Enter the location: ")
earthlocation = coord.EarthLocation.of_site(location)
# Creates the ime object
# [mjd] is where you put the time, format can change 
# format can be 'jd', 'mjd', 'decimalyear', 'datetime', and more
# scale can be 'tdb' or 'tcb' but will probably be utc
print("To change the format to mjd or decimal years, please manually change the code")
time1 = eval(input("Enter the time you want to convert: "))
times = time.Time([time1], format='jd', scale='utc',location=earthlocation)

#FOR HJD
# This calculates the change in time from MJD to HJD
# This adds the change in times to your original time
choice = eval(input("Enter 1 for HJD or 2 for BJD. "))
if choice == 1: 
    ltt_helio= times.light_travel_time(ip_peg, 'heliocentric')
    time_heliocenter = times.utc + ltt_helio
    print(time_heliocenter)

# FOR BJD
if choice == 2:
    ltt_bary = times.light_travel_time(ip_peg)
    time_barycenter = times.tdb + ltt_bary
    print(time_barycenter)