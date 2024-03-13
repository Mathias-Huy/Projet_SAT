from matplotlib import pyplot as plt
import utils

f = open("Gaz.txt")
bdd = {}

for line in f:
    if not line.startswith("#"):
        line = line.replace(",", ".")
        line = line.split()
        name = line[0]
        ks = [float(x) for x in line[1:-1]]
        masse_mol = float(line[-1])
        index = utils.refraction(name, ks)
        bdd[name] = utils.Gaz(name, masse_mol, index)
f.close()

comp_air_std = [(bdd["O2"], 0.2), (bdd["N2"], 0.8)]
comp_air_co = [(bdd["O2"], 0.189), (bdd["N2"], 0.711), (bdd["CO"], 0.1)]


# Pour l'atmosphère standard : 

atmosphere_std = utils.Atmo(0, 30, comp_air_std)
atmosphere_std.decoupe_altitude(30)
atmosphere_std.profil_indice()

pressions = atmosphere_std.pressions
temperatures = atmosphere_std.temperatures
indices = atmosphere_std.indices
altitudes = atmosphere_std.altitudes

# Pour l'atmosphère avec couche de monoxyde de carbone CO :

atmosphere_std_1 = utils.Atmo(0, 10, comp_air_std)
atmosphere_co = utils.Atmo(10, 20, comp_air_co)
atmosphere_std_2 = utils.Atmo(20, 30, comp_air_std)
atmosphere_std_1.decoupe_altitude(10)
atmosphere_co.decoupe_altitude(10)
atmosphere_std_2.decoupe_altitude(10)
atmosphere_std_1.profil_indice()
atmosphere_co.profil_indice()
atmosphere_std_2.profil_indice()

indices_co = atmosphere_std_1.indices + atmosphere_co.indices + atmosphere_std_2.indices

modele_itu = utils.ITU(pressions, temperatures)

plt.figure("Température")
plt.plot(temperatures, altitudes)
plt.title("Température en fonction de l'altitude")
plt.xlabel("Température en K")
plt.ylabel("Altitude en km")

plt.figure("Pression")
plt.plot([i / 100 for i in pressions], altitudes)
plt.title("Pression en fonction de l'altitude")
plt.xscale("log")
plt.xlabel("Pression en hPa")
plt.ylabel("Altitude en km")

plt.figure("Réfractivité")
plt.plot(indices, altitudes, label = "Indices")
plt.plot(modele_itu, altitudes, ls=':', label = "modèle ITU")
plt.plot(indices_co, altitudes, label = "Indices CO")
plt.title("Réfractivité en fonction de l'altitude")
plt.xlabel("Réfractivité en N unit")
plt.ylabel("Altitude en km")
plt.legend()
plt.show()
