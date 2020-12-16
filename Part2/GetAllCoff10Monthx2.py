from Part2 import Part2Functions as p2
import progressbar


listofgldasdicts = []
listofekkodicts = []
# Iterating over all 10 gldas files and 10 ecco files
for files in range(1, 11):
    fecco = open("../datafiles/ekkofiles/ECCO" + str(files) + ".txt", "r")
    dictecco = {}
    for x in fecco:
        y = x.split()
        # long lat -> value
        dictecco[(float(y[0]), float(y[1]))] = float(y[2])
    listofekkodicts.append(dictecco)
    fecco.close()
    fgldas = open("../datafiles/gldasfiles/2010_0" + str(files) + ".txt", "r")
    dictgldas = {}
    for x in fgldas:
        y = x.split()
        # long lat -> value
        if 32767.000 != float(y[2]):
            dictgldas[(float(y[0]), float(y[1]))] = float(y[2])
    listofgldasdicts.append(dictgldas)
    fgldas.close()

counter = 1
# Calculating coeffs for all files
for n in progressbar.progressbar(range(0, 10)):
    dict1 = listofgldasdicts[0]
    p2.getallcofs(dict1, counter, Gldas=True)
    counter += 1
counter = 1
for n in progressbar.progressbar(range(0, 10)):
    dict1 = listofekkodicts[0]
    p2.getallcofs(dict1, counter, Gldas=False)
    counter += 1
