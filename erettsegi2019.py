from datetime import datetime, timedelta

# 1. feladat: Adatok beolvasása és tárolása
autok = []
with open('autok.txt', 'r') as file:
    for line in file:
        nap, ido, rendszam, szemely, km, ki_be = line.strip().split()
        autok.append({
            'nap': int(nap),
            'ido': ido,
            'rendszam': rendszam,
            'szemely': int(szemely),
            'km': int(km),
            'ki_be': int(ki_be)
        })

# 2. feladat: Utoljára elvitt autó
utolso_kivitel = max((auto for auto in autok if auto['ki_be'] == 0), key=lambda x: (x['nap'], x['ido']))
print("2. feladat")
print(f"{utolso_kivitel['nap']}. nap rendszám: {utolso_kivitel['rendszam']}")

# 3. feladat: Adott napi forgalom
print("\n3. feladat")
nap = int(input("Nap: "))
print(f"Forgalom a(z) {nap}. napon:")
for auto in autok:
    if auto['nap'] == nap:
        irany = "ki" if auto['ki_be'] == 0 else "be"
        print(f"{auto['ido']} {auto['rendszam']} {auto['szemely']} {irany}")

# 4. feladat: Hónap végén kint lévő autók száma
kint_levo_autok = set(auto['rendszam'] for auto in autok if auto['ki_be'] == 0) - set(auto['rendszam'] for auto in autok if auto['ki_be'] == 1)
print("\n4. feladat")
print(f"A hónap végén {len(kint_levo_autok)} autót nem hoztak vissza.")

# 5. feladat: Autónkénti megtett távolság
print("\n5. feladat")
tavolsagok = {}
for auto in autok:
    if auto['rendszam'] not in tavolsagok:
        tavolsagok[auto['rendszam']] = 0
    if auto['ki_be'] == 1:
        tavolsagok[auto['rendszam']] += auto['km'] - max((a['km'] for a in autok if a['rendszam'] == auto['rendszam'] and a['ki_be'] == 0 and (a['nap'], a['ido']) <= (auto['nap'], auto['ido'])), default=0)

for rendszam, tavolsag in tavolsagok.items():
    print(f"{rendszam} {tavolsag} km")

# 6. feladat: Leghosszabb út
print("\n6. feladat")
max_tavolsag = 0
max_szemely = None
for i in range(len(autok)):
    if autok[i]['ki_be'] == 0:
        for j in range(i+1, len(autok)):
            if autok[j]['rendszam'] == autok[i]['rendszam'] and autok[j]['szemely'] == autok[i]['szemely'] and autok[j]['ki_be'] == 1:
                tavolsag = autok[j]['km'] - autok[i]['km']
                if tavolsag > max_tavolsag:
                    max_tavolsag = tavolsag
                    max_szemely = autok[i]['szemely']
                break

print(f"Leghosszabb út: {max_tavolsag} km, személy: {max_szemely}")

# 7. feladat: Menetlevél készítése
print("\n7. feladat")
rendszam = input("Rendszám: ")
with open(f"{rendszam}_menetlevel.txt", 'w') as file:
    for i in range(len(autok)):
        if autok[i]['rendszam'] == rendszam and autok[i]['ki_be'] == 0:
            ki_datum = f"{autok[i]['nap']}. {autok[i]['ido']}"
            ki_km = autok[i]['km']
            for j in range(i+1, len(autok)):
                if autok[j]['rendszam'] == rendszam and autok[j]['szemely'] == autok[i]['szemely'] and autok[j]['ki_be'] == 1:
                    be_datum = f"{autok[j]['nap']}. {autok[j]['ido']}"
                    be_km = autok[j]['km']
                    file.write(f"{autok[i]['szemely']}\t{ki_datum}\t{ki_km} km\t{be_datum}\t{be_km} km\n")
                    break

print("Menetlevél kész.")
