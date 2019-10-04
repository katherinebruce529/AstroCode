#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 12:46:30 2019

@author: katherinebruce
"""

from astropy.io import fits
import numpy as np
from astropy import units as u
from astropy.nddata import CCDData
import ccdproc
import astropy.nddata

# Hello welcome to by big processing code
# SALT has a flat made for it, and DOES NOT need overscan or zero
# preflat = Yes, everything else No
# MDM has a flat made for it, and needs overscan
# preflat = Yes, oscan= yes
# CTIO needs flat combination and zero subtraction
# DEPENDS, no oscan tho. 

# Deciding which route to take
oneorno = input("For single image processing, enter 'Yes': ")
print("CTIO, SALT, MDM")
telescope = input("Enter the telescope data you're using: ")
if telescope == 'SALT':
    anszero = 'No'
    preflat = 'Yes'
    ansflat = 'No'
    ansover = 'No'
    ansflat = 'No'
if telescope == 'CTIO':
    prezero = input("Do you have a pre-made zero? Yes or No: ")
    preflat = input("Do you have a pre-made flat? Yes or No: ")
    anszero = 'No'
    if preflat == 'No':
        ansflat = 'Yes'
    if preflat != 'No':
        ansflat = 'No'
    if prezero == 'No':
        anszero = 'Yes'
    if prezero != 'No':
        anszero = 'No'
if telescope == 'MDM':
    preflat = 'Yes'
    ansover = 'Yes'
if anszero == 'Yes':
    print('\n')
    print("ZERO COMBINE")
    print('\n')
    # Takes in the file and reads all of the image files off of it
    list1 = input("Enter a .txt file with the ZERO image paths and names: ")
    filelist = []
    infile = open(list1,'r')
    for line in infile: 
        line = line.strip('\n')
        filelist.append(line)
    filearray = [] 
    nimages = len(filelist)
    # Reads all of the files as fits files
    # Turns the fits data into a numpy array and creates
    # A list of all the numpy array
    for n in range(nimages):
        im = fits.getdata(filelist[n])
        im = np.array(im)
        filearray.append(im)
    # One just numpy array of numpy arrays
    all = np.array(filearray)
    # Median combines them into one numpy array
    # Which can be turned back into a fits file
    zero = np.median(all, axis=0)
    # Start the rejection process
    # Decide how many mins and maxes to reject 
    print('Rejection values, min-max rejection')
    print('Rejects the given number of minimum and maximum valeus')
    nlow = eval(input("Enter the low value (0 Recommend): "))
    nhigh = eval(input("Enter the high value (1 Recommend): "))
    upper = zero.max()
    lower = zero.min()
    # Replace the rejected pixels with the median value
    replace = np.median(zero)
    # Iterate over how many mins and maxs are being rejected
    for i in range(nhigh):
        zero = np.where(zero == upper, replace, zero)
        upper = zero.max()
    for i in range(nlow):
        zero = np.where(zero == lower, replace, zero)
        lower = zero.min()
    outfile = input("Enter the output file path and name: ")
    # Write the numpy array into a fits file 
    # And the zero is done!
    fits.writeto(outfile, zero)
if ansover == 'Yes':
    print('\n')
    print('OVERSCAN CORRECTION')
    print('\n')
    # Input the .txt file and turn it into a list of image paths
    if oneorno != 'Yes':
        list11 = input("Enter a .txt file with the SCIENCE images paths and names: ")
        filelist = []
        infile = open(list11,'r')
        for line in infile: 
            line = line.strip('\n')
            filelist.append(line)
        filearray = []
        headerlist = []
        # Iterate over the list of paths to get all of the data
        # From the fits file and from the headers
        for n in range(len(filelist)):
            file = fits.open(filelist[n])
            im = fits.getdata(filelist[n])
            im = CCDData(im, unit=u.dimensionless_unscaled)
            filearray.append(im)
            file.close()
            hdr = file[0].header
            headerlist.append(hdr)
        # Read the needed info from the headers
        xsize = file[0].header['NAXIS1']
        ysize = file[0].header['NAXIS2']
        overscanx = file[0].header['OVERSCNX']
        overscany = file[0].header['OVERSCNY']
        print("Enter the path and name of the files. Each file will be saved with sequction numbers and the extension")
        print("So just put the name you want the file and the computer will add  'overscan0.fits' and so on")
        # Iterate over how many files there are
        for n in range(len(filearray)):
            im = filearray[n]
            outover = im.replace('.fits','')
            # If the overscan is in the x direction
            if overscanx != 0:
                # Find the edge of the image where the overscan is
                x2 = xsize - overscanx
                # Subtract the overscan from the image
                oscan = ccdproc.subtract_overscan(im, overscan=im[0:ysize,x2:xsize],overscan_axis=1)
                # Save the image
                astropy.nddata.fits_ccddata_writer(oscan,outover+ 'overscan' + str(n) + '.fits')
                # Paste the header into the new file
                file2 = fits.open(outover+ 'overscan' + str(n) + '.fits')
                hdu2 = file2[0].header
                hdu2.clear()
                hdu2.extend(headerlist[n])
                file2.close()
            # If the overscan is in the y direction
            if overscany != 0:
                # Find the edge of the iamge where the overscan is
                y2 = ysize - overscany
                # Subtract the overscan from the image
                oscan = ccdproc.subtract_overscan(im, overscan=im[0:xsize,y2:ysize],overscan_axis=1)
                # Save the image
                astropy.nddata.fits_ccddata_writer(oscan,outover+ 'overscan' + str(n) + '.fits')
                # Paste the header into the new file
                file2 = fits.open(outover+ 'overscan' + str(n) + '.fits', mode = 'update')
                hdu2 = file2[0].header
                hdu2.extend(headerlist[n])
                file2.close()
    if oneorno == 'Yes':
        filedata = input("Enter the image path and name: ")
        file = fits.open(filedata)
        im = fits.getdata(filedata)
        im = CCDData(im, unit=u.dimensionless_unscaled)
        file.close()
        hdr = file[0].header
        # Read the needed info from the headers
        xsize = file[0].header['NAXIS1']
        ysize = file[0].header['NAXIS2']
        overscanx = file[0].header['OVERSCNX']
        overscany = file[0].header['OVERSCNY']
        print("Enter the path and name of the files. Each file will be saved with sequction numbers and the extension")
        print("So just put the name you want the file and the computer will add  'overscan0.fits' and so on")
        outover = filedata.replace('.fits','')
        # Iterate over how many files there are
        # If the overscan is in the x direction
        if overscanx != 0:
            # Find the edge of the image where the overscan is
            x2 = xsize - overscanx
            # Subtract the overscan from the image
            oscan = ccdproc.subtract_overscan(im, overscan=im[0:ysize,x2:xsize],overscan_axis=1)
            # Save the image
            astropy.nddata.fits_ccddata_writer(oscan,outover+ 'overscan.fits')
            # Paste the header into the new file
            file2 = fits.open(outover+ 'overscan.fits')
            hdu2 = file2[0].header
            hdu2.clear()
            hdu2.extend(hdr)
            file2.close()
        # If the overscan is in the y direction
        if overscany != 0:
            # Find the edge of the iamge where the overscan is
            y2 = ysize - overscany
            # Subtract the overscan from the image
            oscan = ccdproc.subtract_overscan(im, overscan=im[0:xsize,y2:ysize],overscan_axis=1)
            # Save the image
            astropy.nddata.fits_ccddata_writer(oscan,outover+ 'overscan .fits')
            # Paste the header into the new file
            file2 = fits.open(outover + 'overscan.fits', mode = 'update')
            hdu2 = file2[0].header
            hdu2.extend(hdr)
            file2.close()
if ansflat == 'Yes':
    print('\n')
    print("FLAT COMBINE")
    print('\n')
    # Take in the list of paths/images from a .txt file
    list1 = input("Enter a .txt file with the FLAT image paths and names: ")
    filelist = []
    infile = open(list1,'r')
    for line in infile: 
        line = line.strip('\n')
        filelist.append(line)
    filearray = [] 
    # Get all the data from the fits files and turn them into numpy arrays
    for n in range(len(filelist)):
        im = fits.getdata(filelist[n])
        im = np.array(im)
        filearray.append(im)
    # Create a numpy array of numpy arrays
    all = np.array(filearray)
    # Median combine the numpy arrays to one numpy array
    flat = np.median(all, axis=0)
    # Rejection time
    #Rejects pixels out of a certain range of standard deviations
    print('Rejection values, sigclip reject')
    print('Rejects values outside of of the standard devaition (sigma)')
    print('Until all values fall within this range')
    print('If using science images to create a flat DO NOT use rejection')
    # COMMENT FROM HERE 
    signum = eval(input("How many sigmas do you want to clip? Recommended 4 to 5: "))
    # Reject the max and min first
    minreject = flat.min()
    maxreject = flat.max()
    replace = np.median(flat)
    flat = np.where(flat == minreject, replace, flat)
    flat = np.where(flat == maxreject, replace, flat)
    # Then reject any values outside of the range of St.Dev.
    standev = signum * flat.std()
    upper = np.median(flat) + standev
    lower = np.median(flat) - standev
    median = np.median(flat)
    IsDone = False
    # Keep doing this and re-calculating the median 
    # Until every value is inside the St.Dev. range
    while IsDone == False:
        flat[flat > upper] = median
        flat[flat < lower] = median
        standev = signum * flat.std()
        upper = median + standev
        lower = median - standev
        median = np.median(flat)
        if flat.max() <= upper and flat.min() >= lower:
            IsDone = True
    # TO HERE IF USING SCIENCE IMAGES
    # Normalize the flat by dividing by the median value
    median = np.median(flat)
    flat = flat/median
    # Save the new fits file
    outfile = input("Enter the output file path and name: ")
    fits.writeto(outfile, flat)
print('\n')
print("IMAGE CORRECTON")
print('\n')
if prezero == 'Yes':
    zero = input("Enter the path and file name of your zero: ")
    zero = fits.open(zero)
    zero = zero[0].data
    zero = np.array(zero)
if preflat == 'Yes':
    flat = input("Enter the path and file name of your flat: ")
    flat = fits.open(flat)
    flat = flat[0].data
    flat = np.array(flat)
# Enter inputs and outputs
print("If you did overscan correction, enter the list or image with the NEW science images that end in 'overscan0.fits' etc")
if oneorno != 'Yes':
    if ansover == 'No':
        ims = input("Enter a .txt file with the SCIENCE image paths and names: ")
        print("Enter the path you want and the file name you want, the code will add the extension, '0.fits' and so on" )
        # Read the input images 
        filelist = []
        headerlist = []
        infile = open(ims,'r')
        for line in infile: 
            line = line.strip('\n')
            filelist.append(line)
    if ansover == 'Yes':
        fielist = []
        headerlist = []
        for i in range(len(list11)):
            ims = outover+ 'overscan' + str(i) + '.fits'
            filelist.append(line)
if oneorno == 'Yes':
    if ansover == 'No':
        filelist = input('Enter the SCIENCE image path and name: ')
        print("Enter the path you want and the file name you want, the code will '.fits'" )
    if ansover == 'Yes':
        filelist = outover + 'overscan.fits'
# If you did zero and flat
if anszero == 'Yes' and ansflat == 'Yes' and ansover == 'No' and preflat == 'No' and prezero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Subtract the zero
            im = im - zero
            # Divide by the flat
            im = im / flat
            # Save the new fits image
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        hdr = im[0].header
        im = im[0].data
        im = np.array(im)
        # Subtract the zero
        im = im - zero
        # Divide by the flat
        im = im / flat
        # Save the new fits image
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out + 'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
if anszero == 'No' and ansflat == 'Yes' and ansover == 'Yes' and preflat == 'No' and prezero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Divide by the flat
            im = im / flat
            # Save the new file
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            # Copy the header over
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        hdr = im[0].header
        im = im[0].data
        im = np.array(im)
        # Divide by the flat
        im = im / flat
        # Save the new file
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+ 'processed.fits'
        # Copy the header over
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# If you just did zero
if anszero == 'Yes' and ansflat == 'No' and ansover == 'No' and preflat == 'No' and prezero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data 
            im = np.array(im)
            # Subtract the zero
            im = im - zero
            # Save the image
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            # Copy the header over
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the data
        im = fits.open(filelist)
        hdr = im[0].header
        im = im[0].data 
        im = np.array(im)
        # Subtract the zero
        im = im - zero
        # Save the image
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header
        outfile = out + 'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# If you just did flats
if anszero == 'No' and ansflat == 'Yes' and ansover == 'No' and preflat == 'No' and prezero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Divide by the flat
            im = im / flat
            # Save the new file
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            # Copy the header over
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        im = fits.open(filelist)
        hdr = im[0].header
        headerlist.append(hdr)
        im = im[0].data
        im = np.array(im)
        # Divide by the flat
        im = im / flat
        # Save the new file
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# If you had premade zero
if prezero == 'Yes' and preflat == 'No' and ansover == 'No' and ansflat == 'No' and anszero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
        # Import the data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Subtract the zero
            im = im - zero
            # Save the image
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the data
        im = fits.open(filelist)
        hdr = im[0].header
        im = im[0].data
        im = np.array(im)
        # Subtract the zero
        im = im - zero
        # Save the image
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# If you had a premade flat 
if preflat == 'Yes' and prezero == 'No' and ansover == 'No' and ansflat == 'No' and anszero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            # flat = flat[:,:-4] FOR SALT STUFF
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[1].data
            im = np.array(im)
            # Divide by the flat
            im = im / flat
            # Save the new file
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        # flat = flat[:,:-4] FOR SALT STUFF
        hdr = im[0].header
        im = im[1].data
        im = np.array(im)
        # Divide by the flat
        im = im / flat
        # Save the new file
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# if you had a premade flat and zero
if preflat == 'Yes' and prezero == 'Yes' and ansover == 'No' and ansflat == 'No' and anszero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Subtract the zero
            im = im - zero
            # Divide by the flat
            im = im / flat
            # Save the new fits image
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        hdr = im[0].header
        headerlist.append(hdr)
        im = im[0].data
        im = np.array(im)
        # Subtract the zero
        im = im - zero
        # Divide by the flat
        im = im / flat
        # Save the new fits image
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# if you had a premade zero and created a flat
if preflat == 'No' and prezero == 'Yes' and ansover == 'No' and ansflat == 'Yes' and anszero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data        
            im = np.array(im)
            # Subtract the zero
            im = im - zero
            # Divide by the flat
            im = im / flat
            # Save the new fits image
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        hdr = im[0].header
        im = im[0].data        
        im = np.array(im)
        # Subtract the zero
        im = im - zero
        # Divide by the flat
        im = im / flat
        # Save the new fits image
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# if you had a premade flat and created a zero
if preflat == 'Yes' and prezero == 'No' and ansover == 'No' and ansflat == 'No' and anszero == 'Yes':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Subtract the zero
            im = im - zero
            # Divide by the flat
            im = im / flat
            # Save the new fits image
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        hdr = im[0].header
        headerlist.append(hdr)
        im = im[0].data
        im = np.array(im)
        # Subtract the zero
        im = im - zero
        # Divide by the flat
        im = im / flat
        # Save the new fits image
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()
# if you had a premade flat and did overscan
if preflat == 'Yes' and prezero == 'No' and ansover == 'Yes' and ansflat == 'No' and anszero == 'No':
    if oneorno != 'Yes':
        for n in range(len(filelist)):
            # Import the fits data
            im = fits.open(filelist[n])
            hdr = im[0].header
            headerlist.append(hdr)
            im = im[0].data
            im = np.array(im)
            # Divide by the flat
            im = im / flat
            # Save the new file
            outim = filelist[n]
            out = outim.replace('.fits','')
            fits.writeto(out + 'processed.fits', im)
            # Copy the header over
            outfile = out+'processed.fits'
            file2 = fits.open(outfile, mode='update')
            hdu2 = file2[0].header
            hdu2.extend(headerlist[n])
            file2.close()
    if oneorno == 'Yes':
        # Import the fits data
        im = fits.open(filelist)
        hdr = im[0].header
        headerlist.append(hdr)
        im = im[0].data
        im = np.array(im)
        # Divide by the flat
        im = im / flat
        # Save the new file
        outim = filelist
        out = outim.replace('.fits','')
        fits.writeto(out + 'processed.fits', im)
        # Copy the header over
        outfile = out+'processed.fits'
        file2 = fits.open(outfile, mode='update')
        hdu2 = file2[0].header
        hdu2.extend(hdr)
        file2.close()