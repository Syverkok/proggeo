import math as mt
from Part1 import Part1Functions
import pandas as pd
import progressbar
import numpy as np
a = 637100079.00


f = open("../datafiles/love_number.txt", "r")
count = 0
lovenumlist = []
for x in f:
    y = x.split()
    if count >= 6:
        lovenumlist.append(float(y[1][:-4])*10**-2)
    else:
        lovenumlist.append(float(y[1]))
    count = count + 1
f.close()

# Function for calculating the coefficients R and Q
def getcoff(n, m, coff, valdict):
    constant = 1 / (4 * mt.pi) * ((1 + lovenumlist[n]) / (2 * n + 1)) * ((3 * 1000) / (a * 5517))
    sm = 0
    for key in valdict:
        if 0 <= mt.radians(key[0]) <= 2*mt.pi and -mt.pi/2 <= mt.radians(key[1]) <= mt.pi/2:
            if coff == 'R':
                sm = sm + valdict[key] * Part1Functions.get_p_bar(n, m, mt.radians(key[1]), mt.sin(mt.radians(key[1]))) \
                     * mt.cos(m*mt.radians(key[0])) * mt.cos(mt.radians(key[1])) * (mt.pi/180) ** 2
            else:
                sm = sm + valdict[key] * Part1Functions.get_p_bar(n, m, mt.radians(key[1]), mt.sin(mt.radians(key[1]))) \
                     * mt.sin(m * mt.radians(key[0])) * mt.cos(mt.radians(key[1])) * (mt.pi / 180) ** 2
    return constant*sm
# Another approach for coefficients calculation, give the same results.
def getcoff2(n, m, coff, valdict):
    constant = 1 / (4 * mt.pi) * ((1 + lovenumlist[n]) / (2 * n + 1)) * ((3 * 1000) / (a * 5517))
    sm = 0
    for lam in np.arange(0.5, 360.5, 1 ):
        for phi in np.arange(-89.5, 90.5, 1 ):
            key = (lam, phi)
            try:
                if coff == 'R':
                    sm = sm + valdict[key] * Part1Functions.get_p_bar(n, m, mt.radians(key[1]), mt.sin(mt.radians(key[1]))) \
                         * mt.cos(m*mt.radians(key[0])) * mt.cos(mt.radians(key[1])) * (mt.pi/180) ** 2
                else:
                    sm = sm + valdict[key] * Part1Functions.get_p_bar(n, m, mt.radians(key[1]), mt.sin(mt.radians(key[1]))) \
                         * mt.sin(m * mt.radians(key[0])) * mt.cos(mt.radians(key[1])) * (mt.pi / 180) ** 2
            except:
                pass
    return constant * sm

# Function which calculates all coefficients for one file.
def getallcofs(dictinput, monthnub, Gldas = True):
    cofflist = []
    for n in progressbar.progressbar(range(0, 101)):
        for m in range(0, n+1):
            rcof = getcoff(n, m, 'R', dictinput)
            qcof = getcoff(n, m, 'Q', dictinput)
            cofflist.append([n, m, rcof, qcof])
    df = pd.DataFrame(cofflist, columns=['N', 'M', 'R', 'Q'])
    if Gldas:
        df.to_csv('../datafiles/Results/Coffs/Gldas_' + str(monthnub) + '.csv', sep='\t', index=False, header=False)
        with open('../datafiles/Results//Coffs/Gldas_' + str(monthnub) + '.tex', 'w') as tf:
            tf.write(df.to_latex(index=False))
    else:
        df.to_csv('../datafiles/Results/Coffs/Ecco_' + str(monthnub) + '.csv', sep='\t', index=False, header=False)
        with open('../datafiles/Results/Coffs/Ecco_' + str(monthnub) + '.tex', 'w') as tf:
            tf.write(df.to_latex(index=False))


# Function for calculating Sigma/ Roe Water, used for validating the coefficients
def calculate_sigmaoverro(lam, phi, coffdict):
    sum_tot = 0
    for n in progressbar.progressbar(range(0, 101)):
        for m in range(0, n + 1):
            sum_tot += (coffdict.get((n, m))[0] * mt.cos(m * lam) + coffdict.get((n, m))[1]*mt.sin(m * lam)) * \
                       Part1Functions.get_p_bar(n, m, phi, mt.sin(phi)) * (2 * n + 1) / (1 + lovenumlist[n])

    return (sum_tot * 5517*a/3)/1000
