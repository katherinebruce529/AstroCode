#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 11:11:19 2019

@author: katiebruce
"""
import pandas as pd

choice = eval(input("Enter 1 for CV single, enter 2 for CV .csv file, enter 3 for Vis single, enter 4 for vis .cvs file: "))

if choice == 1:
    ctar = eval(input("Enter the CV magnitude: "))
    vcomp = eval(input("Enter the V mag of the comp: "))
    bcomp = eval(input("Enter the B-V mag of the comp: "))
    bminvtar = eval(input("Enter the B-V of the target: "))
    deltc = ctar - vcomp
    deltbminv = bminvtar - (bcomp)
    vtar = deltc + (0.37 * deltbminv) + vcomp
    print("V Mag")
    print(vtar)
    btar = vtar + bminvtar
    print("B Mag")
    print(btar)
    
if choice == 2:
    mags = input("Enter the .csv path and file name: ")
    df = pd.read_csv(mags,index_col=False)
    col = input("Enter the magnitude column name: ")
    vcomp = eval(input("Enter the V mag of the comp: "))
    bcomp = eval(input("Enter the B-V mag of the comp: "))
    bminvtar = eval(input("Enter the B-V of the target: "))
    transformedv = []
    transformedb = []
    for i in range(len(df)):
        ctar = df[col][i]
        deltc = ctar - vcomp
        deltbminv = bminvtar - (bcomp)
        vtar = deltc + (0.37 * deltbminv) + vcomp
        transformedv.append(vtar)
        btar = vtar + bminvtar
        transformedb.append(btar)
    transformedv = pd.DataFrame(transformedv)
    transformedv.columns = ['Vmag']
    df = df.join(transformedv)
    transformedb = pd.DataFrame(transformedb)
    transformedb.columns = ['Bmag']
    df = df.join(transformedb)
    del df[col]
    outfile = input("Enter the output path and name: ")
    df.to_csv(outfile, index=False)

if choice == 3:
    vistar = eval(input("Enter the visual mag of the target: "))
    bminvtar = eval(input("Enter the B-V of the target: "))
    Vmag = vistar - (0.21 * bminvtar)
    print(Vmag)
    Bmag = Vmag + bminvtar
    print(Bmag)
    
if choice == 4:
    mags = input("Enter the .csv path and file name: ")
    df = pd.read_csv(mags,index_col=False)
    col = input("Enter the magnitude column name: ")
    bminvtar = eval(input("Enter the B-V of the target: "))
    bminvtar = float(bminvtar)
    transformedv = []
    transformedb = []
    for i in range(len(df)):
        vistar = df[col][i]
        Vmag = vistar - (0.21 * bminvtar)
        transformedv.append(Vmag)
        Bmag = Vmag + bminvtar
        transformedb.append(Bmag)
    transformedv = pd.DataFrame(transformedv)
    transformedv.columns = ['Vmag']
    df = df.join(transformedv)
    transformedb = pd.DataFrame(transformedb)
    transformedb.columns = ['Bmag']
    df = df.join(transformedb)
    del df[col]
    outfile = input("Enter the output path and name: ")
    df.to_csv(outfile, index=False)