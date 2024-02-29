import math as m
import numpy as np

R = 8, 31446261815324  # J K−1 mol−1
masse_molaire_air = 29e-3


class Gas:

    def __init__(self, name, density, index, compr):
        self.name = name
        self.density_ctrl = float(density) if density != "None" else None
        self.index_ctrl = float(index) if index != "None" else None
        self.env_ctrl = (self.index_ctrl, self.density_ctrl)
        self.compr = float(compr)
        self.desity = None
        self.masse_molaire = None

