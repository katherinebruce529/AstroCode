#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 10:06:25 2019

@author: katherinebruce
"""
from datetime import date
import pandas as pd

choice = eval(input("For Date-JD enter 1, for JD-Date, enter 2: "))

if choice == 1:
    df = input("Enter the file path and name: ")
    df = pd.read_csv(df, index_col=False) 
    print('Use the column name in the CSV file')
    col = input('Enter the date column name: ')
    sep = input('Enter the separating character: ')
    date1 = []
    for n in range(len(df)):
        splitted = df[col][n].split(sep)
        year = int(splitted[0])
        month = int(splitted[1])
        day = int(splitted[2])
        a = year // 100
        b = a // 4
        c = 2 - a + b
        e = int(365.25 * (year + 4716))
        f = int(30.6001 * (month + 1))
        jd = c + day + e + f - 1524
        date1.append(jd)
    date1 = pd.DataFrame(date1)
    df = df.join(date1)
    # Deletes the date column
    # Comment this to keep the dates
    del df[col]
    # Saves as a new CSV
    outfile = input("Enter the output path and name: ")
    df.to_csv(outfile, index=False)

if choice == 2:
    # Enter the CSV file
    df = input("Enter the file path and name: ")
    df = pd.read_csv(df, index_col=False) 
    print('Use the column name in the CSV file')
    col = input('Enter the JD column name: ')
    date1 = []
    # This calculates all of the dates
    for n in range(len(df)):
        jd = int(df[col][n])
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
        date1.append(x)
    # Saves the new column as 'Date'
    df['Date'] = pd.to_datetime(date1)
    # Deletes the JD column
    # Comment this to keep the JDs
    del df[col]
    # Saves as a new CSV
    outfile = input("Enter the output path and name: ")
    df.to_csv(outfile, index=False)
