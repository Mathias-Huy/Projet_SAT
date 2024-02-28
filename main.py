from Gas import Gas
import math as m

bdd = []


def init_gaz(liste):
    fichier = open("Gaz.txt")
    for line in fichier:
        line = line.replace(",", ".")
        data = line.split()
        x = Gas(data[0], data[2], data[3], data[1])
        liste.append(x)
    fichier.close()


def ciddor(panache):
    l = 0
    for gaz in panache:
        l += (gaz.density / gaz.density_ctrl) * (((gaz.index_ctrl ** 2) - 1) / ((gaz.index_ctrl ** 2) + 2))

    return l


def lorenz_lorentz(panache):
    l = ciddor(panache)
    indice = m.sqrt((1 - 2 * l) / (1 - l))
    return indice


init_gaz(bdd)
