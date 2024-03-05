from math import *
import matplotlib.pyplot as plt

import utils

sigma = 1 / 0.6  # m^-1
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

#Atmosphère standard de 0 à 30 km d'altitude :

comp_air = [(bdd["O2"], 0.22), (bdd["N2"], 0.78)]
# air_std = utils.Atmo(0, 30, comp_air)
# air_std.decoupe(300)

# for tranche in air_std.tranche:
#     altitude.append(tranche[0])
#     p.append(tranche[1])
#     t.append(tranche[2])
#     L = 0
#     P = 0
#     print(tranche)
#     for gaz_tup in air_std.comp:
#         gaz = gaz_tup[0]
#         coeff = gaz_tup[1]
#         pression_partiel = coeff * tranche[1]  # pression en hPa
#         P += pression_partiel
#         temperature = tranche[2]

#         dens = utils.density(pression_partiel, temperature, gaz.masse_mol)
#         L += gaz.ciddor(dens)
#     print(P)
#     indice = (sqrt((1 + 2 * L) / (1 - L))-1)*10**6
#     indices.append(indice)

## Atmosphère divisée en trois couches de 0 à 30 km d'altitude :

#une couche d'air "classique" de 0 à 10km d'altitude
    
air_std_1 = utils.Atmo(0, 10, comp_air) 
air_std_1.decoupe(100)
 
for tranche in air_std_1.tranche:
    altitude.append(tranche[0])
    p.append(tranche[1])
    t.append(tranche[2])
    L = 0
    P = 0
    for gaz_tup in air_std_1.comp:
        gaz = gaz_tup[0]
        coeff = gaz_tup[1]
        pression_partiel = coeff * tranche[1]  # pression en hPa
        P += pression_partiel
        temperature = tranche[2]

        dens = utils.density(pression_partiel, temperature, gaz.masse_mol)
        L += gaz.ciddor(dens)
    indice = (sqrt((1 + 2 * L) / (1 - L))-1)*10**6
    indices.append(indice)

#une deuxième couche d'air composée à 50% de monoxyde de carbone de 10 à 20 km d'altitude

comp_air_co = [(bdd["O2"], 0.11), (bdd["N2"], 0.39), (bdd["CO"], 0.50)]
air_co = utils.Atmo(10, 20, comp_air_co) 
air_co.decoupe(100)

for tranche in air_co.tranche:
    altitude.append(tranche[0])
    p.append(tranche[1])
    t.append(tranche[2])
    L = 0
    P = 0
    
    for gaz_tup in air_co.comp:
        gaz = gaz_tup[0]
        coeff = gaz_tup[1]
        pression_partiel = coeff * tranche[1]  # pression en hPa
        P += pression_partiel
        temperature = tranche[2]
         

        dens = utils.density(pression_partiel, temperature, gaz.masse_mol)
        print (dens)
        print("\n")
        L += gaz.ciddor(dens)
        print(L)
        print("\n")
    indice = (sqrt((1 + 2 * L) / (1 - L))-1)*10**6
    indices.append(indice)

#une troisième couche d'air "classique" de 20 à 30 km d'altitude

air_std_2 = utils.Atmo(20, 30, comp_air) 
air_co.decoupe(100)

for tranche in air_std_2.tranche:
    altitude.append(tranche[0])
    p.append(tranche[1])
    t.append(tranche[2])
    L = 0
    P = 0
    print(tranche)
    for gaz_tup in air_std_2.comp:
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


# plt.plot(indices, altitude, ls=':')
# plt.title("Réfractivité en fonction de l'altitude")
# plt.xlabel("Réfractivité")
# plt.ylabel("Altitude en km")
# plt.show()

plt.plot(indices, altitude, ls=':')
plt.title("Réfractivité en fonction de l'altitude")
plt.xlabel("Réfractivité")
plt.ylabel("Altitude en km")
plt.show()