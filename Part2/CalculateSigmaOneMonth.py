from Part2 import Part2Functions
import numpy as np
import pandas as pd
import progressbar
f = open('../datafiles/Results/Coffs/Ecco_2.csv', "r")
coffdict = {}
for x in f:
    y = x.split()
    # n, m -> r, q
    coffdict[(float(y[0]), float(y[1]))] = [float(y[2]), float(y[3])]
f.close()
fgldas = open("../datafiles/ekkofiles/ECCO2.txt", "r")
dictgldas = {}
for x in fgldas:
    y = x.split()
    # long lat -> value
    if 32767.000 != float(y[2]):
        dictgldas[(float(y[0]), float(y[1]))] = float(y[2])
fgldas.close()

resultslist = []
calulatedlist = []
sigmalist = []
# Iterating over every lambda and phi combination in ecoo/gldas file

for key in progressbar.progressbar(dictgldas):
    # Calculate sigma
    calculatedsigma = Part2Functions.calculate_sigmaoverro(key[0], key[1], coffdict)
    # Get measured sigma
    recivedsigma = dictgldas[key]
    resultslist.append([key[0], key[1], calculatedsigma, recivedsigma])
    calulatedlist.append(calculatedsigma)
    sigmalist.append(recivedsigma)

# Storing the reulsts as tex for report
df = pd.DataFrame(resultslist, columns=['Longitude', 'Latitude', 'Calculated Simga/RoW', 'Recieved Sigma/Row'])
with open('../datafiles/Results/Ekko2010.02_Sigma_row.tex', 'w') as tf:
    tf.write(df.to_latex(index=False))
calculated = np.array(calulatedlist)
recived = np.array(sigmalist)

# Getting statistics
diff = np.subtract(calculated, recived)
diffabs = np.abs(diff)
mean = np.mean(diffabs)
biggest = np.max(diffabs)
smallest = np.min(diffabs)
standard = np.std(diff)
print(round(mean, 6))
print(round(biggest, 6))
print(round(smallest, 6))
print(round(standard, 6))

