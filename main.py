from matplotlib import pyplot as plt
import utils

f = open("Gaz.txt")
bdd = {}

for line in f:
    if not line.startswith("#"):
        line = line.replace(",", ".")
        line = line.split()
        name = line[0]
        k0, k1, k2, masse_mol = map(float, line[1:])
        index = utils.refraction(k0, k1, k2)
        bdd[name] = utils.Gaz(name, masse_mol, index)
f.close()

comp_air_std = [(bdd["O2"], 0.21), (bdd["N2"], 0.79)]
comp_air_co = [(bdd["O2"], 0.189), (bdd["N2"], 0.711), (bdd["CO"], 0.1)]

# atmosphere_std = utils.Atmo(0, 30, comp_air_std)
# atmosphere_std.decoupe_altitude(30)
# atmosphere_std.profil_indice()
# temperature = atmosphere_std.temperatures
# pressions = atmosphere_std.pressions
# indices = atmosphere_std.indices

atmosphere_std_1 = utils.Atmo(0, 10, comp_air_std)
atmosphere_co = utils.Atmo(10, 20, comp_air_co)
atmosphere_std_2 = utils.Atmo(20, 30, comp_air_std)
atmosphere_std_1.decoupe_altitude(10)
atmosphere_co.decoupe_altitude(10)
atmosphere_std_2.decoupe_altitude(10)
atmosphere_std_1.profil_indice()
atmosphere_co.profil_indice()
atmosphere_std_2.profil_indice()

pressions = atmosphere_std_1.pressions + atmosphere_co.pressions + atmosphere_std_2.pressions
temperatures = atmosphere_std_1.temperatures + atmosphere_co.temperatures + atmosphere_std_2.temperatures
indices = atmosphere_std_1.indices + atmosphere_co.indices + atmosphere_std_2.indices
altitudes = atmosphere_std_1.altitudes + atmosphere_co.altitudes + atmosphere_std_2.altitudes

modele_itu = utils.ITU(pressions, temperatures)

plt.figure("Temperature")
plt.plot(temperatures, altitudes)
plt.title("Temperature en fonction de l'altitude")
plt.xlabel("Temperature en K")
plt.ylabel("Altitude en km")

plt.figure("Pression")
plt.plot([i / 100 for i in pressions], altitudes)
plt.title("Pression en fonction de l'altitude")
plt.xscale("log")
plt.xlabel("Pression en hPa")
plt.ylabel("Altitude en km")

plt.figure("Réfractivité")
plt.plot(indices, altitudes)
plt.plot(modele_itu, altitudes, ls=':')
plt.title("Réfractivité en fonction de l'altitude")
plt.xlabel("Réfractivité en N unit")
plt.ylabel("Altitude en km")

plt.show()
