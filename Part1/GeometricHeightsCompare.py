from Part1 import Part1Functions
import math as mt
import numpy as np
import pandas as pd
import progressbar
pointsdict = {}
nmdictGGM = {}
nmdictEGM = {}
# Open the GPS EGM and GGM files

f = open("../datafiles/GNSS data.txt", "r")
f2 = open("../datafiles/GGM03S.gfc.txt", "r")
f3 = open("../datafiles/EGM2008.gfc.txt", "r")


# Reading each line in the files and store in dict
for x in f:
    y = x.split()
    # Storing phi lam - > ortho h, elips h
    pointsdict[(float(y[1]), float(y[2]))] = [float(y[3]), float(y[4])]
f.close()
for x in f2:
    y = x.split()
    # n & m -> C & S
    nmdictGGM[(float(y[1]), float(y[2]))] = [float(y[3]), float(y[4])]
f2.close()
for x in f3:
    y = x.split()
    # n & m -> C & S

    nmdictEGM[(float(y[1]), float(y[2]))] = [float(y[3]), float(y[4])]
f3.close()


ggm_list = []
egm_list = []
gps_list = []
resultslist = []
# Iterating over every lambda and phi combination in gps file
for key in progressbar.progressbar(pointsdict):
    # Getting h ortho and h elips
    h_orto = pointsdict[key][0]
    h_elips = pointsdict[key][1]
    Part1Functions.p_dict = {}
    # Getting gravimetric heights
    ggm = Part1Functions.get_n2(mt.radians(float(key[0])), mt.radians(float(key[1])), nmdictGGM, 180)
    egm = Part1Functions.get_n2(mt.radians(float(key[0])), mt.radians(float(key[1])), nmdictEGM, 2000)
    # Calculating geometric height
    gps = h_elips-h_orto
    ggm_list.append(ggm)
    egm_list.append(egm)
    gps_list.append(gps)
    # lat long ggm egm gps data
    resultslist.append([key[0], key[1], ggm, egm , gps, ggm-gps, egm-gps])
df = pd.DataFrame(resultslist, columns=['Latitude', 'Longitude', 'Geoid Height GGM', 'Geoid Height EGM',
                                        'Geoid Height GPS', 'ggm-gps', 'egm-gps'])
df.to_csv('../datafiles/Results/EGMGGMGPS', sep='\t', header=False, index=False)
with open('../datafiles/Results/EGMGGMGPS.tex','w') as tf:
    tf.write(df.to_latex(index = False))

ggm = np.array(ggm_list)
egm = np.array(egm_list)
geoidmodellsit = [ggm, egm]
strlist = ['GGM', 'EGM']

gps = np.array(gps_list)
# Calculating statistics for both models
for i in range(0, 2):
    diff = np.subtract(geoidmodellsit[i], gps)
    diffabs = np.abs(diff)
    mean = np.mean(diffabs)
    biggest = np.max(diffabs)
    smallest = np.min(diffabs)
    standard = np.std(diff)
    print(strlist[i])
    print(round(mean, 6))
    print(round(biggest, 6))
    print(round(smallest, 6))
    print(round(standard, 6))
    i += 1





