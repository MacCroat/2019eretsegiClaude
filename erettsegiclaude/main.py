from datetime import datetime, timedelta


# 1. feladat: Adatok beolvasása
def beolvas():
    autok = []
    with open('autok.txt', 'r') as file:
        for sor in file:
            nap, ido, rendszam, szemely, km, irany = sor.strip().split()
            autok.append({
                'nap': int(nap),
                'ido': ido,
                'rendszam': rendszam,
                'szemely': int(szemely),
                'km': int(km),
                'irany': int(irany)
            })
    return autok


# 2. feladat: Utolsó kivitt autó
def utolso_kivitt_auto(autok):
    utolso = max((auto for auto in autok if auto['irany'] == 0), key=lambda x: (x['nap'], x['ido']))
    print(f"2. feladat")
    print(f"{utolso['nap']}. nap rendszám: {utolso['rendszam']}")


# 3. feladat: Napi forgalom
def napi_forgalom(autok, nap):
    print(f"3. feladat")
    print(f"Nap: {nap}")
    print(f"Forgalom a(z) {nap}. napon:")
    for auto in autok:
        if auto['nap'] == nap:
            irany = "ki" if auto['irany'] == 0 else "be"
            print(f"{auto['ido']} {auto['rendszam']} {auto['szemely']} {irany}")


# 4. feladat: Hónap végén kint lévő autók
def kint_levo_autok(autok):
    kint = set()
    for auto in autok:
        if auto['irany'] == 0:
            kint.add(auto['rendszam'])
        else:
            kint.discard(auto['rendszam'])
    print(f"4. feladat")
    print(f"A hónap végén {len(kint)} autót nem hoztak vissza.")


# 5. feladat: Megtett távolságok
def megtett_tavolsagok(autok):
    tavolsagok = {f"CEG30{i}": 0 for i in range(10)}
    utolso_km = {f"CEG30{i}": 0 for i in range(10)}

    for auto in autok:
        if auto['irany'] == 0:
            utolso_km[auto['rendszam']] = auto['km']
        else:
            tavolsagok[auto['rendszam']] += auto['km'] - utolso_km[auto['rendszam']]

    print("5. feladat")
    for rendszam, tavolsag in tavolsagok.items():
        print(f"{rendszam} {tavolsag} km")


# 6. feladat: Leghosszabb út
def leghosszabb_ut(autok):
    utak = {}
    for i in range(len(autok) - 1):
        if autok[i]['irany'] == 0 and autok[i + 1]['irany'] == 1 and autok[i]['rendszam'] == autok[i + 1]['rendszam']:
            tavolsag = autok[i + 1]['km'] - autok[i]['km']
            utak[autok[i]['szemely']] = max(utak.get(autok[i]['szemely'], 0), tavolsag)

    leghosszabb = max(utak.items(), key=lambda x: x[1])
    print("6. feladat")
    print(f"Leghosszabb út: {leghosszabb[1]} km, személy: {leghosszabb[0]}")


# 7. feladat: Menetlevél készítése
def menetlevel_keszites(autok, rendszam):
    with open(f"{rendszam}_menetlevel.txt", 'w') as file:
        for i in range(len(autok) - 1):
            if autok[i]['rendszam'] == rendszam and autok[i]['irany'] == 0:
                for j in range(i + 1, len(autok)):
                    if autok[j]['rendszam'] == rendszam and autok[j]['irany'] == 1:
                        ki_datum = f"{autok[i]['nap']}. {autok[i]['ido']}"
                        be_datum = f"{autok[j]['nap']}. {autok[j]['ido']}"
                        file.write(
                            f"{autok[i]['szemely']}\t{ki_datum}\t{autok[i]['km']} km\t{be_datum}\t{autok[j]['km']} km\n")
                        break
    print("7. feladat")
    print(f"Rendszám: {rendszam}")
    print("Menetlevél kész.")


# Főprogram
def main():
    autok = beolvas()
    utolso_kivitt_auto(autok)

    nap = int(input("Nap: "))
    napi_forgalom(autok, nap)

    kint_levo_autok(autok)
    megtett_tavolsagok(autok)
    leghosszabb_ut(autok)

    rendszam = input("Rendszám: ")
    menetlevel_keszites(autok, rendszam)


if __name__ == "__main__":
    main()