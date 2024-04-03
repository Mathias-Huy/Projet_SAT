from matplotlib import pyplot as plt
import utils

f = open("Gaz.txt")
bdd = {}
nb_de_tranche = 30
altitude_deb = 0
altitude_fin = 30
altitudes = [0 + i * ((altitude_fin - altitude_deb) / nb_de_tranche) for i in range(nb_de_tranche)]
pressions = [utils.modele_pression(altitude) for altitude in altitudes]
temperatures = [utils.modele_temperature(altitude) for altitude in altitudes]

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
# Pour l'atmosphère avec couche de monoxyde de carbone CO :

taux = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1]

atmosphere_std_1 = utils.Tranche_Atmo(0, 10, comp_air_std, nb_de_tranche // 3)
atmosphere_std_2 = utils.Tranche_Atmo(20, 30, comp_air_std, nb_de_tranche // 3)
atmospheres_etude = []

for x in taux:
    # On cree diferente atmosphère avec des differend taux de CO
    comp_air_co = [(bdd["O2"], 0.2 * (1 - x)), (bdd["N2"], 0.8 * (1 - x)), (bdd["CO"], x)]
    atmo = utils.Tranche_Atmo(10, 20, comp_air_co, nb_de_tranche // 3)
    # Condition aux limites.
    atmo_cplt = utils.Atmo([atmosphere_std_1, atmo, atmosphere_std_2])
    atmospheres_etude.append(atmo_cplt)

atmo_std = atmospheres_etude[1]
"""La Codition au limite est encore fausse, il faudrai revoir encore ça"""
# On trace les profils de temperature et pressions
utils.plot_profils_temp_pressions(altitudes, temperatures, pressions)

utils.variation_itu(atmospheres_etude, taux)

# On trace le profil de refractivité de l'atmo avec Panache
utils.plot_profil_indices(atmo_std)

# utils.plot_grad(indices_co, altitudes_co)

plt.show()
