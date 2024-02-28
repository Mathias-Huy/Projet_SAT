import math
import numpy as np
from Gas import Gas

R = 8, 31446261815324  # J/K/mol la constante des gazs parfaits
masse_molaire_air = 29e-3  # kg/mol
masse_vol_air = 1.204  # kg/m^3


def density(pression, temperature, masse_molaire, compres=1):
    masse_vol = (masse_molaire * pression) / (R * temperature * compres)

    return masse_vol / masse_vol_air
