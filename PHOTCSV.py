#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 12:59:38 2019

@author: katherinebruce
"""

# You must activate astroconda before running this code
# This code performs photometry on multiple images with multiple comparison stars 
# ONLY IF the coordinates are the same between images
# The program accepts a .txt file with the image names and paths
# And outputs a .txt file with the pixel values, comparative magnitudes 
# With each comparison star and a short statistical analysis

from photutils import CircularAperture
from photutils import aperture_photometry
from astropy.io import fits
import math
import pandas as pd

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
    im = input('Enter the science image path and name: ')
# Determine comparison stars and target coordinates
df = input("Enter the coordinate and mag file path and name: ")
df = pd.read_csv(df, index_col=False)

num_comp = len(df) - 1
coord_targetx = df['XCoord'][0]
coord_targety = df['YCoord'][0]
positions = [(coord_targetx, coord_targety)]
comp_mag = []
for i in range(num_comp):
    maggy = df['Mag'][i+1]
    xcoord = df['XCoord'][i+1]
    ycoord = df['YCoord'][i+1]
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
        # Create a file to save 
        image = image.replace('.fits','')
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
    image = image.replace('.fits','')
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
