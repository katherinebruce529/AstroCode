#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 10:50:58 2019

@author: katherinebruce
"""
# This code performs photometry on multiple images with multiple comparison stars 
# ONLY IF the coordinates are the same between images
# The program accepts a .txt file with the image names and paths
# And outputs a .txt file with the pixel values, comparative magnitudes 
# With each comparison star and a short statistical analysis
#
# Use this to get the FWHM and the coords of the stars
# Type the uncommented lines into the ipython shell

#import imexam
#viewer = imexam.connect()
#viewer.load_fits(im)
#viewer.imexam()

# In the xgterm ds9 window
# Hover over the star you want to look at
# X returns the x value
# Y returns the y value
# J gives the Gaussian fit and FWHM

from photutils import CircularAperture
from photutils import aperture_photometry
from astropy.io import fits
import math
import numpy as np 
# accept the .txt file
oneorno = input("For single image processing, enter 'Yes': ")
if oneorno != 'Yes':
    list1 = input("Enter a .txt file with the image paths and names: ")
    filelist = []
    infile = open(list1,'r')
    # create a list of the filenames
    for line in infile: 
        line = line.strip('\n')
        filelist.append(line)
if oneorno == 'Yes':
    im = input('Enter the .fits science image path and name: ')
# Determine comparison stars and target coordinates
num_comp = eval(input("How many comparison stars are you using? "))
coord_targetx = eval(input("Enter the target x coordinate: "))
coord_targety = eval(input("Enter the target y coordinate: "))
positions = [(coord_targetx, coord_targety)]
comp_mag = []
for i in range(num_comp):
    maggy = eval(input("Enter the magnitude of comparison star " + str(i+1) + ": "))
    xcoord = eval(input("Enter the x coordinate of comparison star " + str(i+1) + ": "))
    ycoord = eval(input("Enter the y coordinate of comparison star " + str(i+1) + ": "))
    coords = (xcoord, ycoord)
    positions.append(coords)
    comp_mag.append(maggy)
ap = eval(input("Enter the aperature size: "))
# Create the aperature
aperture = CircularAperture(positions, r=ap)
# Run the aperature photometry for each file
if oneorno != 'Yes':
    for i in range(len(filelist)):
        image = filelist[i]
        image = str(image)
        im = fits.getdata(image)
        phot_table = aperture_photometry(im,aperture)
        # Save the pixel values from the table
        flux = []
        target_flux = phot_table[0][3]
        for i in range(num_comp):
            ff = phot_table[i+1][3]
            flux.append(ff)
        phot_table = str(phot_table)
        # Create a file to save to
        file = open(image + "phot.txt",'w')
        file.write(phot_table)
        file.write('\n')
        all = []
        # Turn the pixel values into magnitudes
        for i in range(num_comp):
            logpart = math.log10(target_flux / flux[i])
            mag = (-2.5 * logpart) + comp_mag[i]
            all.append(mag)
            file.write("The target magnitude with comparison star "+ str(i+1) + " is: " + str(mag))
            file.write('\n')
            # Statistical Analysis
        avg = np.mean(all)
        std = np.std(all)
        file.write("The average magnitude is " + str(avg))
        file.write('\n')
        file.write("The standard deviation is " + str(std))
        file.write('\n')
        # Close the file
        file.close()
if oneorno == 'Yes':
    image = str(im)
    im = fits.getdata(image)
    phot_table = aperture_photometry(im,aperture)
    # Save the pixel values from the table
    flux = []
    target_flux = phot_table[0][3]
    for i in range(num_comp):
        ff = phot_table[i+1][3]
        flux.append(ff)
    phot_table = str(phot_table)
    # Create a file to save to
    file = open(image + "phot.txt",'w')
    file.write(phot_table)
    file.write('\n')
    all = []
    # Turn the pixel values into magnitudes
    for i in range(num_comp):
        logpart = math.log10(target_flux / flux[i])
        mag = (-2.5 * logpart) + comp_mag[i]
        all.append(mag)
        file.write("The target magnitude with comparison star "+ str(i+1) + " is: " + str(mag))
        file.write('\n')
        # Statistical Analysis
    avg = np.mean(all)
    std = np.std(all)
    file.write("The average magnitude is " + str(avg))
    file.write('\n')
    file.write("The standard deviation is " + str(std))
    file.write('\n')
    # Close the file
    file.close()
