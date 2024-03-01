import utils

sigma = 1 / 600  # m^-1
f = open("Gaz.txt")
bdd = {}
altitude = []
indice = []

for line in f:
    if not line.startswith("#"):
        line = line.replace(",", ".")
        line = line.split()
        name = line[0]
        k0, k1, k2, density, masse_mol = map(float, line[1:])
        index = utils.refrac(k0, k1, k2, sigma)
        bdd[name] = utils.Gas(name, density, index)

f.close()

comp_air = [(bdd["O2"], 0.2), (bdd["N2"], 0.8)]
air_std = utils.Atmo(0, 30, comp_air)
air_std.decoupe(300)

for tranche in air_std.tranche:
    altitude.append(tranche[0])
    L = 0
    for gaz_tup in air_std.comp:
        gaz = gaz_tup[0]
        coeff = gaz_tup[1]
        pression = coeff * tranche[1]
        temperature = tranche[2]
        dens = utils.density(pression, temperature, gaz.masse_mol)
        L+=

print(bdd)
