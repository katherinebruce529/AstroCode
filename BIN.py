#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 21 10:30:30 2019

@author: katherinebruce
"""
# This program bins data by day, month, year, or a custom amount
# Dates must be in JD, MJD, or HJD
# This program accepts only csv files
# This program outputs only csv files

import pandas as pd
# Accept file
df = input("Enter the file path and name: ")
df = pd.read_csv(df, index_col=False)
# Determine speficifations of file
num = input("How many columns are there? ")
date = input("What is your date column called? ")
bintype = input("How are you binning: Day, Month, Year or enter a custom number? ")
# Determine binning type
# And bin by that type
if bintype == 'Day':
    df[date] = df[date].astype(int)
elif bintype == 'Month':
    df[date] = df[date].apply(lambda x: x//30)
elif bintype == 'Year':
	df[date] = df[date].apply(lambda x: x//365)
elif bintype > 0:
    df[date] = df[date].apply(lambda x: x//bintype)
agg = {}
# Create a list of the other columns
# Which will be combined by the mean
for i in range(int(num)-1):
     col = input("Enter other column names: ")
     agg.update({col : 'mean'})
# Combine the columns by like numbers
binned = df.groupby(df[date]).aggregate(agg)
# Take the date out of the index
binned = binned.reset_index()
# Convert back to JD, MJD, or HJD
# Depending on the binning type
if bintype == 'Day':
    binned[date] = binned[date].astype(int)
elif bintype == 'Month':
    binned[date] = binned[date].apply(lambda x: x*30)
elif bintype == 'Year':
    binned[date] = binned[date].apply(lambda x: x*365)
elif bintype > 0:
    binned[date] = binned[date].apply(lambda x: x*bintype)
# Save to a new csv file
savepath = input("Enter save path and .csv file name: ")
binned.to_csv(savepath, index=False)
