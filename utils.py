import math as m
import numpy as np

"""On initialise les gaz pour une longueur d'onde de 60m"""

R = 8.31446261815324  # J/K/mol la constante des gazs parfaits
masse_vol_air = 1204  # g/m^3


class Gas:

    def __init__(self, name, dens, index, mas_mol):
        self.name = name
        self.density_ctrl = float(dens) if density != "None" else None
        self.index_ctrl = float(index) if index != "None" else None
        self.env_ctrl = (self.index_ctrl, self.density_ctrl)
        self.masse_mol = mas_mol

    def ciddor(self, densite):
        return (densite / self.density_ctrl) * ((self.index_ctrl ** 2 - 1) / (self.index_ctrl ** 2 + 2))


class Atmo:

    def __init__(self, altitude_deb, altitude_fin, liste):
        """altitude en km"""
        self.debut = altitude_deb
        self.fin = altitude_fin
        self.comp = liste
        self.tranche = None

    def decoupe(self, tranche):
        self.tranche = []
        pas = (self.fin - self.debut) / tranche
        for x in range(tranche):
            self.tranche.append(
                (self.debut + x * pas, pression(self.debut + x * pas), temperature(self.debut + x * pas)))


def density(press, temp, masse_molaire, compres=1.):
    masse_vol = (masse_molaire * press * 100) / (R * temp * compres)
    return masse_vol


def refrac(k0, k1, k2, sigma):
    return 1 + 10e-8 * (k0 + (k1 / (k2 - sigma ** 2)))


def temperature(altitude_geom):
    """altitude en km et retourne la temperature en kelvin"""
    altitude = (6356.766 * altitude_geom) / (6356.766 + altitude_geom)
    if altitude < 11:
        return 288.15 - 6.5 * altitude
    elif 11 <= altitude < 20:
        return 216.65
    elif 20 <= altitude < 32:
        return 216.65 + 2.8 * (altitude - 20)


def pression(altitude_geom):
    """Pression en hPa avec l'altitude en km"""
    altitude= (6356.766*altitude_geom)/(6356.766+altitude_geom)
    if altitude <= 11:
        return 1013.25 * (288.15 / (288.15 - 6.5 * altitude)) ** (-34.1632 / 6.5)
    elif 11 < altitude <= 20:
        return 226.3226 * m.exp(-34.1632 * (altitude - 11) / 216.65)
    elif 20 < altitude <= 32:
        return 54.74980 * (216.65 / (216.65 + (altitude - 20))) ** 34.1632
