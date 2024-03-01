import math as m
import numpy as np

"""On initialise les gaz pour une longueur d'onde de 60m"""

R = 8, 31446261815324  # J/K/mol la constante des gazs parfaits
masse_molaire_air = 29e-3  # kg/mol
masse_vol_air = 1.204  # kg/m^3


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


def density(press, temp, masse_molaire, compres=1):
    masse_vol = (masse_molaire * press) / (R * temp * compres)

    return masse_vol / masse_vol_air


def refrac(k0, k1, k2, sigma):
    return 1 + 10e-8 * (k0 + (k1 / (k2 - sigma ** 2)))


def temperature(altitude):
    """altitude en km et retourne la temperature en kelvin"""
    if altitude < 13:
        return 294.9838 - 5.2159 * altitude - 0.07109 * altitude ** 2
    elif 13 <= altitude < 17:
        return 215.5
    elif 17 <= altitude < 47:
        return 215.5 * m.exp((altitude - 17) * 0.008128)


def pression(altitude):
    """Pression en hPa avec l'altitude en km"""

    if altitude <= 10:
        return 1012.8186 - 111.5569 * altitude + 3.8646 * altitude ** 2
    elif 10 < altitude <= 72:
        return pression(10) * m.exp(-0.417 * (altitude - 10))
