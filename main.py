from matplotlib import pyplot as plt
import utils

f = open("Gaz.txt")
bdd = {}
nb_de_tranche = 30

for line in f:
    if not line.startswith("#"):
        line = line.replace(",", ".")
        line = line.split()
        name = line[0]
        ks = [float(x) for x in line[1:-1]]
        masse_mol = float(line[-1])
        indice_ctrl = utils.refraction(name, ks)
        bdd[name] = utils.Gaz(name, masse_mol, indice_ctrl)
f.close()

comp_air_std = [(bdd["O2"], 0.2), (bdd["N2"], 0.8)]

# Pour l'atmosphère standard :

atmosphere_std = utils.Atmo(0, 30, comp_air_std, nb_de_tranche)
atmosphere_std.profil_indice()

pressions = atmosphere_std.pressions
temperatures = atmosphere_std.temperatures
indices = atmosphere_std.indices
altitudes = atmosphere_std.altitudes

# Pour l'atmosphère avec couche de monoxyde de carbone CO :

taux = [0, 0.1, 0.2, 0.3, 0.4, 0.5]

atmosphere_std_1 = utils.Atmo(0, 10, comp_air_std, nb_de_tranche // 3)
atmosphere_std_2 = utils.Atmo(20, 30, comp_air_std, nb_de_tranche // 3)
atmospheres_co = []

for x in taux:
    # On cree diferente atmosphère avec des differend taux de CO
    comp_air_co = [(bdd["O2"], 0.2 * 1 - x), (bdd["N2"], 0.8 * (1 - x)), (bdd["CO"], x)]
    atmo = utils.Atmo(10, 20, comp_air_co, nb_de_tranche // 3)
    # Condition aux limites.
    atmo.condition_limite(atmosphere_std_1, atmosphere_std_2)
    atmospheres_co.append(atmo)

utils.del_prem_elem(atmosphere_std_1, atmosphere_std_2)



pressions_co = atmosphere_std_1.pressions + atmospheres_co[0].pressions + atmosphere_std_2.pressions
temperatures_co = atmosphere_std_1.temperatures + atmospheres_co[0].temperatures + atmosphere_std_2.temperatures
indices_co = atmosphere_std_1.indices + atmospheres_co[0].indices + atmosphere_std_2.indices
altitudes_co = atmosphere_std_1.altitudes + atmospheres_co[0].altitudes + atmosphere_std_2.altitudes

# Modele fourni par l'ITU
modele_itu = utils.ITU(pressions, temperatures)

# On trace les profils de temperature et pressions
utils.plot_profils_temp_pressions(altitudes, temperatures, pressions)

# On trace le profil de refractivité de l'atmo std
utils.plot_profil_indices(indices, altitudes, modele_itu)

utils.variation_itu(atmosphere_std_1, atmosphere_std_2, atmospheres_co, modele_itu, taux)


# On trace le profil de refractivité de l'atmo avec Panache
#utils.plot_profil_indices(indices_co, altitudes_co, modele_itu)

plt.show()
