import math as m
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

"""On initialise les gaz pour une longueur d'onde de 60m"""

R = 8.31446261815324  # J/K/mol la constante des gazs parfaits
frequence = 5e6  # en Hz
lambd = 3e8 / frequence
sigma = 1 / (lambd * 10 ** 2)
anorm = [(-3, 0), (-4.5,1), (-5, 2), (-5.5,3), (-6, 4), (-6, 5), (-6, 6), (-6.5, 7), (-7, 8), (-8,9), (-7, 10), (-3,10.5), (0,11), (5,11.5), (9, 12), (10, 13), (9, 14),
         (8, 15), (7.5, 16), (6,17), (5, 18), (4, 19), (3, 20), (2, 21), (0.5, 22), (0, 23), (0, 24), (0.5,25), (1.5, 26), (2, 27), (-1, 28), (1, 29), (0, 30)]
temp_anorm = [a[0] for a in anorm]
alt_anorm = [a[1] for a in anorm]

fill_value="extrapolate"
fonction_anom_temperature = interp1d(alt_anorm, temp_anorm, kind='linear')
plt.ion()


class Gaz:

    def __init__(self, name, masse_molaire, indice_ctrl, ):
        self.name = name
        self.masse_molaire = masse_molaire  # en kg/mol
        self.masse_volumique_ctrl = self.calc_masse_volumique(101325, 290)  # en kg/m^3
        self.indice_ctrl = indice_ctrl

    def calc_masse_volumique(self, pression, temperature):
        """Donne la masse volumique d'un gaz en kg/m^3 en fonction de la pression en Pa de la temperature en K et de
        la constante R"""

        return (pression * self.masse_molaire) / (R * temperature)

    def ciddor(self, masse_volumique):
        """Determine le L de chaque gaz a l'aide d'une masse volumique en kg/m^3"""

        return (masse_volumique / self.masse_volumique_ctrl) * (
                (self.indice_ctrl ** 2 - 1) / (self.indice_ctrl ** 2 + 2))


class Tranche_Atmo:

    def __init__(self, altitude_debut, altitude_fin, composition, nb_tranche, anom_temp=False):
        self.indices = None
        self.temperatures = None
        self.pressions = None
        self.altitudes = None
        self.altitude_debut = altitude_debut
        self.altitude_fin = altitude_fin
        self.composition = composition
        self.anom_temp = anom_temp
        self.decoupe_altitude(nb_tranche)

    def decoupe_altitude(self, nombre_de_tranche):
        pas = (self.altitude_fin - self.altitude_debut) / nombre_de_tranche
        self.altitudes = [self.altitude_debut + (i * pas) for i in
                          range(nombre_de_tranche + 1)]

        self.profil_indice()

    def profil_pression(self):
        self.pressions = []  # liste des Pressions en Pa

        for altitude in self.altitudes:
            self.pressions.append(modele_pression(altitude))

    def profil_temperature(self):
        self.temperatures = []  # Liste des temperature en K

        if self.anom_temp:
            anomalie = fonction_anom_temperature(self.altitudes)

            for i in range(len(self.altitudes)):
                temperatures = modele_temperature(self.altitudes[i])
                self.temperatures.append(temperatures + anomalie[i])
        else:
            for altitude in self.altitudes:
                self.temperatures.append(modele_temperature(altitude))

    def profil_indice(self):
        self.indices = []
        self.profil_pression()
        self.profil_temperature()

        for i in range(len(self.altitudes)):
            L = 0
            for gaz, coeff in self.composition:
                pression = self.pressions[i]
                temperature = self.temperatures[i]
                pression_partielle = pression * coeff  # Pression partielle du gaz en Pa
                masse_volumique = gaz.calc_masse_volumique(pression_partielle, temperature)  # Masse Volumique en kg/m^3
                L += gaz.ciddor(masse_volumique)

            indice = m.sqrt((1 + (2 * L)) / (1 - L))

            indice = (indice - 1) * (10 ** 6)
            self.indices.append(indice)


class Atmo:

    def __init__(self, atmosphere):
        self.atmosphere_complete = atmosphere
        self.altitudes = []
        self.indices = []
        self.temperatures = []
        self.condition_limite()
        self.concatene_indices()
        self.concatene_altitude()
        self.concatene_temp()

    def condition_limite(self):
        for i in range(1, len(self.atmosphere_complete)):
            atmo_av = self.atmosphere_complete[i]
            # del atmo_av.indices[-1], \
            #     atmo_av.altitudes[-1], \
            #     atmo_av.pressions[-1], \
            #     atmo_av.temperatures[-1]

    def concatene_altitude(self):
        for atmo in self.atmosphere_complete:
            self.altitudes = self.altitudes + atmo.altitudes[:-1]

    def concatene_indices(self):
        for atmo in self.atmosphere_complete:
            self.indices = self.indices + atmo.indices[:-1]

    def concatene_temp(self):
        for atmo in self.atmosphere_complete:
            self.temperatures = self.temperatures + atmo.temperatures[:-1]


def modele_pression(altitude_geom):
    """Pression en Pa avec l'altitude en km"""
    altitude = (6356.766 * altitude_geom) / (6356.766 + altitude_geom)
    if altitude <= 11:
        return (1013.25 * (288.15 / (288.15 - 6.5 * altitude)) ** (-34.1632 / 6.5)) * 100
    elif 11 < altitude <= 20:
        return (226.3226 * m.exp(-34.1632 * (altitude - 11) / 216.65)) * 100
    elif 20 < altitude <= 32:
        return (54.74980 * (216.65 / (216.65 + (altitude - 20))) ** 34.1632) * 100


def modele_temperature(altitude_geom):
    """altitude en km et retourne la temperature en kelvin"""
    altitude = (6356.766 * altitude_geom) / (6356.766 + altitude_geom)
    if altitude < 11:
        return 288.15 - 6.5 * altitude
    elif 11 <= altitude < 20:
        return 216.65
    elif 20 <= altitude < 32:
        return 216.65 + (altitude - 20)


def ITU(pressions, temperatures):
    std = []
    for i in range(len(pressions)):
        x = 77.6 * (pressions[i] / (temperatures[i] * 100))
        std.append(x)
    return std


def refraction(name, ks):
    k0, k1, k2, k3, k4, k5, k6, k7, k8, k9, k10 = ks
    if name == "Dry":
        return 1 + (k1 / (k0 - (sigma ** 2))) + (k3 / (k2 - (sigma ** 2)))
    elif name == "CO2":
        return 1 + k0 * (10 ** -3) * (
                (k1 / (k2 ** 2 - (sigma ** 2))) + (k3 / (k4 ** 2 - sigma ** 2)) + (k5 / (k6 ** 2 - (sigma ** 2))) + (
                k7 / (k8 ** 2 - (sigma ** 2))) + (k9 / (k10 ** 2 - (sigma ** 2))))
    else:
        return 1 + (10 ** -8) * (k0 + (k1 / (k2 - (sigma ** 2))))


# alt_anorm_interpolated = np.linspace(min(alt_anorm), max(alt_anorm), 100)
# temp_anorm_interpolated = f_cubic(alt_anorm_interpolated)

def anomalie_temperature(altitude):
    temp_anorm_interpolated = fonction_anom_temperature(altitude)

    return temp_anorm_interpolated


def plot_profils_temp_pressions(altitudes, temperatures, pressions):
    # Création des subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 6))

    # Graphique de température
    ax1.plot(temperatures, altitudes)
    ax1.set_title("Température en fonction de l'altitude")
    ax1.grid(True)
    ax1.set_xlabel("Température en K")
    ax1.set_ylabel("Altitude en km")

    # Graphique de pression
    ax2.plot([i / 100 for i in pressions], altitudes)
    ax2.set_title("Pression en fonction de l'altitude")
    ax2.grid(True)
    ax2.set_xscale("log")
    ax2.set_xlabel("Pression en hPa")

    ax3.plot(fonction_anom_temperature(altitudes), altitudes, label="Données Document")
    #ax3.plot(temp_anorm, alt_anorm, label="Fonction interpolée")
    ax3.grid(True)
    ax3.set_title("Anomalie de Temperature")
    ax3.set_xlabel("Déviation de Temperature")
    plt.legend()



def plot_profil_indices(atmo):
    # Nous allons tracer le modèle de l'ITU
    altitudes = atmo.altitudes
    pressions = [modele_pression(altitude) for altitude in altitudes]
    temperatures = [modele_temperature(altitude) for altitude in altitudes]
    modele_itu = ITU(pressions, temperatures)

    plt.figure("Réfractivité")
    plt.plot(atmo.indices, altitudes, label="Indices")
    plt.plot(modele_itu, altitudes, ls=':', label="modèle ITU")
    plt.title("Réfractivité en fonction de l'altitude")
    plt.xlabel("Réfractivité en N unit")
    plt.ylabel("Altitude en km")
    plt.legend()
    plt.grid()


def variation_itu(atmos_etude, taux):
    plt.figure("Variation par rapport au modèle de l'ITU")
    plt.ylabel("Altitude en km")
    plt.xlabel("Ecart au modele ITU")
    for k in range(len(atmos_etude)):
        atmo = atmos_etude[k]
        difference = []
        altitudes = atmo.altitudes
        pressions = [modele_pression(altitude) for altitude in altitudes]
        temperatures = [modele_temperature(altitude) for altitude in altitudes]
        modele_itu = ITU(pressions, temperatures)
        for i in range(len(atmo.indices)):
            difference.append(modele_itu[i] - atmo.indices[i])

        plt.plot(difference, altitudes, label="Taux CO: " + str(taux[k]))
    plt.legend()
    plt.grid()


def plot_grad(indices, altitudes):
    plt.figure("Gradient de Réfractivité")
    plt.title("Gradient de Réfractivité pour 10% de CO")
    plt.ylabel("Altitude en km")
    plt.xlabel("Gradient de Réfractivité")
    grad = np.gradient(indices)
    plt.plot(grad, altitudes)
    plt.grid()
