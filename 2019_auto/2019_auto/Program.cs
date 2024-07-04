using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;

namespace _2019_auto
{
    class Program
    {
        static List<Autó> autók = new List<Autó>();

        static void Main()
        {
            // 1. feladat
            BeolvasAdatokat();

            // 2. feladat
            UtolsóKivitel();

            // 3. feladat
            NapiKimutatás();

            // 4. feladat
            HiányzóAutók();

            // 5. feladat
            Statisztika();

            // 6. feladat
            LeghosszabbÚt();

            // 7. feladat
            Menetlevél();
        }

        static void BeolvasAdatokat()
        {
            string[] sorok = File.ReadAllLines("autok.txt");
            foreach (string sor in sorok)
            {
                string[] adatok = sor.Split(' ');
                autók.Add(new Autó(
                    int.Parse(adatok[0]),
                    adatok[1],
                    adatok[2],
                    int.Parse(adatok[3]),
                    int.Parse(adatok[4]),
                    int.Parse(adatok[5]) == 0
                ));
            }
        }

        static void UtolsóKivitel()
        {
            var utolsóKivitel = autók.FindLast(a => a.Kivitel);
            Console.WriteLine($"2. feladat\n{utolsóKivitel.Nap}. nap rendszám: {utolsóKivitel.Rendszám}");
        }

        static void NapiKimutatás()
        {
            Console.Write("3. feladat\nNap: ");
            int nap = int.Parse(Console.ReadLine());
            Console.WriteLine($"Forgalom a(z) {nap}. napon:");
            var napiForgalom = autók.Where(a => a.Nap == nap);
            foreach (var autó in napiForgalom)
            {
                Console.WriteLine($"{autó.Időpont} {autó.Rendszám} {autó.Személy} {(autó.Kivitel ? "ki" : "be")}");
            }
        }

        static void HiányzóAutók()
        {
            var hiányzóAutók = autók.GroupBy(a => a.Rendszám)
                                    .Count(g => g.Last().Kivitel);
            Console.WriteLine($"4. feladat\nA hónap végén {hiányzóAutók} autót nem hoztak vissza.");
        }

        static void Statisztika()
        {
            Console.WriteLine("5. feladat");
            foreach (var autó in autók.GroupBy(a => a.Rendszám))
            {
                int megtettTáv = autó.Last().Kilométer - autó.First().Kilométer;
                Console.WriteLine($"{autó.Key} {megtettTáv} km");
            }
        }

        static void LeghosszabbÚt()
        {
            var leghosszabbÚt = autók.GroupBy(a => new { a.Rendszám, a.Személy })
                                     .Select(g => new
                                     {
                                         Személy = g.Key.Személy,
                                         Távolság = g.Last().Kilométer - g.First().Kilométer
                                     })
                                     .OrderByDescending(x => x.Távolság)
                                     .First();
            Console.WriteLine($"6. feladat\nLeghosszabb út: {leghosszabbÚt.Távolság} km, személy: {leghosszabbÚt.Személy}");
        }

        static void Menetlevél()
        {
            Console.Write("7. feladat\nRendszám: ");
            string rendszám = Console.ReadLine();
            var menetlevél = autók.Where(a => a.Rendszám == rendszám)
                                  .GroupBy(a => a.Személy)
                                  .Select(g => $"{g.Key}\t{g.First().Nap}. {g.First().Időpont}\t{g.First().Kilométer} km\t{g.Last().Nap}. {g.Last().Időpont}\t{g.Last().Kilométer} km");
            File.WriteAllLines($"{rendszám}_menetlevel.txt", menetlevél);
            Console.WriteLine("Menetlevél kész.");
        }
    }

    class Autó
    {
        public int Nap { get; set; }
        public string Időpont { get; set; }
        public string Rendszám { get; set; }
        public int Személy { get; set; }
        public int Kilométer { get; set; }
        public bool Kivitel { get; set; }

        public Autó(int nap, string időpont, string rendszám, int személy, int kilométer, bool kivitel)
        {
            Nap = nap;
            Időpont = időpont;
            Rendszám = rendszám;
            Személy = személy;
            Kilométer = kilométer;
            Kivitel = kivitel;
        }
    }
}
