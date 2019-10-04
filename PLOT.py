#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 18:34:02 2019

@author: katherinebruce
"""
# This program plots multiple CSV files in one plot with errorbars
# The user can input different variable, such as color, shape, and label
# The most common shapes are as follows
# '.' point 
# 'o' circle
# '^' up triangle
# 'v' down triangle
# 's' square
# 'x' cross
# Colors are 'b' for blue, 'g' for green, and so on
# Also you can just type out the whole color name
# Some variables, such as the linear fit label and color
# Can be manually changed in the code

import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from datetime import date
import numpy as np

erup = input("Does the eruption need to be excluded from the fit? ")
limit = input("Do you have limiting magnitudes? ")
print('Input the columns names in the CSV files')
x_col = input("Enter the x-axis column name: ")
y_col = input("Enter the y-axis column name: ")
err_col = input("Enter error column name: ")
files = input("Enter the path and file name (not limiting): ")
file = pd.read_csv(files)
x_list = file[x_col]
y_list = file[y_col]
err_list = file[err_col]
allx = x_list
ally = y_list
if erup == 'Yes' and limit == 'No':
    jdcut = eval(input("Enter the JD you want to start the fit at: "))
    allx = []
    ally = []
    for j in range(len(x_list)):
        if x_list[j] >= jdcut:
            allx.append(x_list[j])
            ally.append(y_list[j])
if erup == 'Yes' and limit == 'Yes':
    jdcut = eval(input("Enter the JD you want to start the fit at: "))
    allx = []
    ally = []
    for j in range(len(x_list)):
        if x_list[j] >= jdcut:
            allx.append(x_list[j])
            ally.append(y_list[j])
if limit == 'Yes' and erup == 'No':
    allx = []
    for j in range(len(x_list)):
        allx.append(x_list[j])
    ally = []
    for j in range(len(y_list)):
        ally.append(y_list[j])
slope = stats.linregress(allx,ally)
shape = input("Enter the data point shape: ")
col = input("Enter the data set color: ")
mkr = col
if limit == 'Yes':
    mkr = 'None'
fig, ax1 = plt.subplots()
ax1.errorbar(x_list, y_list, yerr=err_list, fmt=shape, color=col)
if limit == 'Yes':
    limiting = input("Enter the limiting mag path and file: ")
    shape2 = input("Enter the data point shape: ")
    col2 = input("Enter the data set color: ")
    limfile = pd.read_csv(limiting)
    xcollim = limfile[x_col]
    ycollim = limfile[y_col]
    errcollim = limfile[err_col]
    plt.errorbar(xcollim, ycollim, yerr=errcollim, fmt=shape2, color=col2, markerfacecolor = 'None', markeredgecolor = col2)
# Comment this to remove the grid
#ax1.grid(True)
# TO CHANGE NUMBER OF TICKS, EDIT THIS
ax1.locator_params(nbins=5)
# This copies the X axis and changes it to dates
ax2 = ax1.twiny()
ax1Xs = ax1.get_xticks()
ax2Xs = []
for X in ax1Xs:
    jd = int(X)
    l = jd + 68569
    n = 4 * l // 146097
    l = l - (146097 * n + 3) // 4
    i = 4000 * (l + 1) // 1461001
    l = l - 1461 * i // 4 + 31
    j = 80 * l // 2447
    k = l - 2447 * j // 80
    l = j // 11
    j = j + 2 - 12 * l
    i = 100 * (n - 49) +i + l
    x = date(i, j, k)
    ax2Xs.append(x)
ax2.set_xticks(ax1Xs)
ax2.set_xticklabels(ax2Xs)
# These name the axes, you can manually change this
ax2.set_xlabel("Date")
ax1.set_xlabel('JD')
ax1.set_ylabel("Magnitude")
# Add other graph specifics
plt.gca().invert_yaxis()
targetname = input("Enter the abbreviated target named: ")
title = targetname + " Long-Term Light Curve"
# Change the type of the values from linregress
# Slope is the stats output, so this is calling the intercept
b = float(slope[1])
m = float(slope[0])
# Plot the linear fit, change the label or color if you want
if erup == 'No':
    jdcut = min(allx)
step = (max(allx) - jdcut)//6
xx = np.arange(jdcut,max(allx), step)
yy = b + m*xx
plt.plot(min(x_list),max(y_list),'x',label='Linear Fit', color = 'white')
plt.plot(max(x_list),min(y_list),'x',label='Linear Fit', color = 'white')
plt.plot(xx,yy,'-',label='Linear Fit', color = 'black')
#plt.xlim(left=jdcut, right=max(x_list))
plt.title(title)
# Comment this to remove the legend
#plt.legend()
# Show the plot and statistical analysis stuff
plt.figure(figsize = (12,16))
plt.show()
print(slope)
# This calculates projected 1 century mag
# And the projected change in mags
end = min(allx) + 36500
begmag = min(allx) * m +b
endmag = (end * m) +b
print("The magnitude one century after the first data point is predicted to be", endmag)
changein = endmag - begmag
print("The projected change in magnitude over one century is", changein)

str1 = "The magnitude one century after the first data point is predicted to be " + str(endmag)
str2 = "The projected change in magnitude over one century is " +  str(changein)
targetname = targetname.replace(' ','')
files = files.replace('.csv','')
file = open(files+ targetname + "stats.txt",'w')
slope = str(slope)
file.write(slope)
file.write('\n')
file.write(str1)
file.write('\n')
file.write(str2)
file.write('\n')
# Close the file
file.close()

