import math
import numpy as np
from Gas import Gas

"""On initialise les gaz pour une longueur d'onde de 60m"""

R = 8, 31446261815324  # J/K/mol la constante des gazs parfaits
masse_molaire_air = 29e-3  # kg/mol
masse_vol_air = 1.204  # kg/m^3


class Gas:

    def __init__(self, name, density, index):
        self.name = name
        self.density_ctrl = float(density) if density != "None" else None
        self.index_ctrl = float(index) if index != "None" else None
        self.env_ctrl = (self.index_ctrl, self.density_ctrl)
        self.desity = None
        self.masse_molaire = None

    def ciddor(self):
        return (self.desity / self.density_ctrl) * ((self.index_ctrl ** 2 - 1) / (self.index_ctrl ** 2 + 2))


def density(pression, temperature, masse_molaire, compres=1):
    masse_vol = (masse_molaire * pression) / (R * temperature * compres)

    return masse_vol / masse_vol_air


def refrac(k0, k1, k2, sigma):
    return 1 + 10e-8 * (k0 + (k1 / (k2 - sigma ** 2)))
