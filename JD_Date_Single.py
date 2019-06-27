#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 08:56:04 2019

@author: katiebruce
"""

choice = eval(input("For Date-JD enter 1, for JD-Date, enter 2: "))

if choice == 1:
    year = eval(input("Enter the year: "))
    month = eval(input("Enter the month: "))
    day = eval(input("Enter the day: "))
    a = year // 100
    b = a // 4
    c = 2 - a + b
    e = int(365.25 * (year + 4716))
    f = int(30.6001 * (month + 1))
    jd = c + day + e + f - 1524
    print(jd)
    
    print("Adding time of day")
    hour = eval(input("Enter the hour in military time: "))
    minute = eval(input("Enter the minutes: "))
    second = eval(input("Enter the seconds: "))
    
    jdt = jd + (hour - 12) / 24 + minute / 1400 + second / 86400
    print(jdt)

if choice == 2:
    jd = eval(input("Enter the JD: "))
    jd = int(jd)
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
    print(i, j, k)
    print("Year month day")

