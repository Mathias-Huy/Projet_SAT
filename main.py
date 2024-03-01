import utils

sigma = 1 / 600  # m^-1
f = open("Gaz.txt")
bdd = {}

for line in f:
    if line[0] == "#":
        pass
    else:
        line.replace(",", ".")
        l = line.split()
        name, k0, k1, k2, density = l[0], float(l[1]), float(l[2]), float(l[3]), float(l[4])
        index = utils.refrac(k0, k1, k2, sigma)
        bdd[name] = utils.Gas(name, density, index)
f.close()

comp_air = [(bdd["O2"], 0.5), (bdd["N2"], 0.5)]
air_std = utils.Atmo(0, 30, comp_air)

tranche = air_std.decoupe(300)

print(bdd)
