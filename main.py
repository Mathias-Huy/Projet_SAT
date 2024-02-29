import utils
from ambiance import Atmosphere

sigma = 1 / 600  # m^-1
f = open("Gaz.txt")
bdd = []

for line in f:
    if line[0] == "#":
        pass
    else:
        l = line.split()
        name, k0, k1, k2, density = l[0], l[1], l[2], l[3], l[4]
        index = utils.refrac(k0, k1, k2)
        bdd.append(utils.Gas(name, density, index))
f.close()

#test