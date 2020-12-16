import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs

# Dicts used to store read values
dictGGM = {}
dictEGM = {}

# Reading file and storing in the two dicts, one for EGM, one for GGM
f = open("../datafiles/Results/geoidheightswrld", "r")
for x in f:
    y = x.split()
    #long lat -> value
    dictGGM[(float(y[0]), float(y[1]))] = float(y[3])
    dictEGM[(float(y[0]), float(y[1]))] = float(y[2])
f.close()


# Vectorizing the data, making it applicable for confourf in cartopy
@np.vectorize
def getVal(phi, lam, dic):
    return dic[lam, phi]

# Creating grid for plotting, which is input in contourf in cartopy

lon = np.arange(-180, 180.5, 0.5)
lat = np.arange(-90, 90.5, 0.5)

'''
lon = np.arange(-20, 10.5, 0.5)
lat = np.arange(45, 65.5, 0.5)
'''
lon2d, lat2d = np.meshgrid(lon, lat)


# Making EGM Map
dataEGM = getVal(lat2d, lon2d, dictEGM)
con = plt.contourf(lon2d, lat2d, dataEGM)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.contourf(lon, lat, dataEGM)
ax.coastlines()
cbar = plt.colorbar(con ,ax=ax, shrink=.55)
cbar.ax.set_ylabel('Meters', rotation=270, labelpad= 15)
#ax.set_extent([-20, 10, 45, 65])
plt.title('EGM2008', fontsize = 20)
#plt.savefig('../datafiles/Results/EGMENGLAND.png')
plt.savefig('../datafiles/Results/EGMWRLDMAP.png')
plt.show()


# Making GGM Map
dataGGM = getVal(lat2d, lon2d, dictGGM)
con = plt.contourf(lon2d, lat2d, dataGGM)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.contourf(lon, lat, dataGGM)
ax.coastlines()
cbar = plt.colorbar(con ,ax=ax, shrink=.55)
cbar.ax.set_ylabel('Meters', rotation=270, labelpad= 15)
#ax.set_extent([-20, 10, 45, 65])
plt.title('GGM03S', fontsize = 20)
#plt.savefig('../datafiles/Results/GGMENGLAND.png')
plt.savefig('../datafiles/Results/GGMWRLDMAP.png')
plt.show()
