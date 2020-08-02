import numpy as np
import matplotlib.pyplot as plt
import time

def solar(INSOLATION, lat, lon, t):
    sun_longitude = (t%DAY)*360/DAY
    value = INSOLATION * np.cos(lat*np.pi/180)*np.cos((lon-sun_longitude)*np.pi/180)

    if value < 0: return 0
    else: return value

SIGMA = 5.67e-8
EPSILON = 0.75
HEAT_CAPACITY_EARTH = 1e5
HEAT_CAPACITY_ATMOS = 1e3
INSOLATION = 1370
PLANET_RADIUS = 6.4e6
DAY = 60*60*24

CIRCLE_AREA = np.pi * PLANET_RADIUS**2
SPHERE_AREA = 4 * np.pi * PLANET_RADIUS**2

t = 0
dt = 60*5

lat = np.arange(-90, 90, 3)
lon = np.arange(0, 360, 3)

nlat, nlon = len(lat), len(lon)

temperature_planet = np.zeros((nlat, nlon))
temperature_atmosp = np.zeros((nlat, nlon))

#####

f, ax = plt.subplots(2)

ax[0].contourf(temperature_planet, x=lat, y=lon, cmap='seismic')
ax[1].contourf(temperature_atmosp, x=lat, y=lon, cmap='seismic')

ax[0].set_title("Ground temperature")
ax[1].set_title("Atmopshere temperature")

plt.ion()
plt.show()

while True:
    for i in range(nlat):
        for j in range(nlon):
            temperature_planet[i,j] += dt*(CIRCLE_AREA * solar(INSOLATION, lat[i], lon[j], t) + SPHERE_AREA * EPSILON * SIGMA * temperature_atmosp[i,j]**4 - SPHERE_AREA * SIGMA * temperature_planet[i,j]**4)/(SPHERE_AREA * HEAT_CAPACITY_EARTH)
            temperature_atmosp[i,j] += dt*(SPHERE_AREA * EPSILON * SIGMA * temperature_planet[i,j]**4 - 2 * SPHERE_AREA * SIGMA * temperature_atmosp[i,j]**4)/(SPHERE_AREA * HEAT_CAPACITY_ATMOS)

    t += dt

    ax[0].contourf(temperature_planet, x=lat, y=lon, cmap='seismic')
    ax[1].contourf(temperature_atmosp, x=lat, y=lon, cmap='seismic')
    
    f.suptitle("Time: " + str(round(t/DAY,2)) + " days")

    plt.pause(0.1)

    ax[0].cla()
    ax[1].cla()
