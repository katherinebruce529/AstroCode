# Image displayer
import matplotlib.pyplot as plt
from astropy.io import fits
import numpy as np 

# accept the .txt file
print("Enter the .txt file without and quotes")
list1 = input("Enter a .txt file with the image paths and names: ")
filelist = []
infile = open(list1,'r')
# create a list of the filenames
for line in infile: 
    line = line.strip('\n')
    filelist.append(line)
for x in range(len(filelist)):
	result = np.array(fits.getdata(filelist[x]))
	print(filelist[x])
	print(x)
	plt.imshow(result, cmap = 'gray')
	plt.show()