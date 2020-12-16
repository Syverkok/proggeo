import numpy as np
from Part1 import Part1Functions
import math as mt
import pandas as pd
import progressbar

# Dictionaries to store the coefficients for each n and m
nmdictGGM = {}
nmdictEGM = {}

# Open the EGM and GGM files
f2 = open("../datafiles/EGM2008.gfc.txt", "r")
f = open("../datafiles/GGM03S.gfc.txt", "r")

# Reading each line in the files and store in dict
for x in f:
    y = x.split()
    # n & m -> C & S
    nmdictGGM[(float(y[1]), float(y[2]))] = [float(y[3]), float(y[4])]
f.close()

for x in f2:
    # n & m -> C & S
    y = x.split()
    nmdictEGM[(float(y[1]), float(y[2]))] = [float(y[3]), float(y[4])]
f.close()

# Iterating over a specified area calculating geoid heights
# The heights are stored in csv file that will be used when plotting the heights to create map of Geoid model
geohighlist = []
#for phi in progressbar.progressbar(np.arange(45, 65.5, 0.5)):
for phi in progressbar.progressbar(np.arange(-90, 90.5, 0.5)):
    # Calculating the p dict for points with same phi
    pfilled_dict = {}
    for n in range(0, 2001):
        for m in range(0, n+1):
            pfilled_dict[n, m] = Part1Functions.get_p_bar(n, m, mt.radians(phi), mt.sin(mt.radians(phi)))
    for lam in np.arange(-180, 180.5, 0.5):
    #for lam in np.arange(-20, 10.5, 0.5):
        negm = Part1Functions.get_n(mt.radians(lam), nmdictEGM, 2000, pfilled_dict)
        nggm = Part1Functions.get_n(mt.radians(lam), nmdictGGM, 180, pfilled_dict)
        # Storing in this order Longitude, Latitude, EGM geoid height, GGM geoid Height
        geohighlist.append([lam, phi, negm, nggm])
df = pd.DataFrame(geohighlist, columns=['Longitude', 'Latitude', 'Geoid Height EGM','Geoid Height GGM'])
#df.to_csv('../datafiles/Results/geoidheightsengland', sep='\t', header=False, index=False)

# Storing the results in CSV and tex for creating map and for report

'''
df.to_csv('../datafiles/Results/geoidheightswrld', sep='\t', header=False, index=False)
# Storing in tex file to show on report
with open('../datafiles/Results/wrldlatex.tex','w') as tf:
    tf.write(df.to_latex(index = False))
'''