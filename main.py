from math import *
import matplotlib.pyplot as plt

import utils

sigma = 1 / 60  # m^-1
f = open("Gaz.txt")
bdd = {}
altitude = []
indices = []
t = []
p = []

for line in f:
    if not line.startswith("#"):
        line = line.replace(",", ".")
        line = line.split()
        name = line[0]
        k0, k1, k2, density, masse_mol = map(float, line[1:])
        index = utils.refrac(k0, k1, k2, sigma)
        bdd[name] = utils.Gas(name, density, index, masse_mol)

f.close()

comp_air = [(bdd["O2"], 0.22), (bdd["N2"], 0.78)]
air_std = utils.Atmo(0, 30, comp_air)
air_std.decoupe(300)

for tranche in air_std.tranche:
    altitude.append(tranche[0])
    p.append(tranche[1])
    t.append(tranche[2])
    L = 0
    P = 0
    print(tranche)
    for gaz_tup in air_std.comp:
        gaz = gaz_tup[0]
        coeff = gaz_tup[1]
        pression_partiel = coeff * tranche[1]  # pression en hPa
        P += pression_partiel
        temperature = tranche[2]

        dens = utils.density(pression_partiel, temperature, gaz.masse_mol)
        L += gaz.ciddor(dens)
    print(P)
    indice = (sqrt((1 + 2 * L) / (1 - L))-1)*10**6
    indices.append(indice)

plt.plot(indices, altitude, ls=':')
plt.title("Réfractivité en fonction de l'altitude")
plt.xlabel("Réfractivité")
plt.ylabel("Altitude en km")
plt.show()
