import math as m
import numpy as np

"""On initialise les gaz pour une longueur d'onde de 60m"""

R = 8.31446261815324  # J/K/mol la constante des gazs parfaits
frequence = 5e9  # en Hz
lambd = 3e8 / frequence
sigma = 1 / lambd


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


class Atmo:

    def __init__(self, altitude_debut, altitude_fin, composition):
        self.indices = None
        self.temperatures = None
        self.pressions = None
        self.altitudes = None
        self.altitude_debut = altitude_debut
        self.altitude_fin = altitude_fin
        self.composition = composition

    def decoupe_altitude(self, nombre_de_tranche):
        pas = (self.altitude_fin - self.altitude_debut) / nombre_de_tranche
        self.altitudes = [self.altitude_debut + (i * pas) for i in
                          range(nombre_de_tranche + 1)]

    def profil_pression(self):
        self.pressions = []  # liste des Pressions en Pa

        for altitude in self.altitudes:
            self.pressions.append(modele_pression(altitude))

    def profil_temperature(self):
        self.temperatures = []  # Liste des temperature en K

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


def refraction(k0, k1, k2):
    return 1 + (10 ** -8) * (k0 + (k1 / (k2 - (sigma ** 2))))


def ITU(pressions, temperatures):
    std = []
    for i in range(len(pressions)):
        x = 77.6 * (pressions[i] / (temperatures[i] * 100))
        std.append(x)
    return std
