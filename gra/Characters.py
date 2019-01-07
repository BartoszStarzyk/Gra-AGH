from gra.Game_functions import pytanie
import random as r


class Opponent:
    def __init__(self, oa, oh):
        self.oa = oa
        self.oh = oh


class Player:
    def __init__(self, pa, pb, pag, ph, name):
        self.pa = pa
        self.pb = pb
        self.pag = pag
        self.ph = ph
        self.name = name

    def walka_1(self, o):
        starting_hp = self.ph
        try:
            while self.ph > 0 and o.oh > 0:
                x = pytanie("[1]: Atak ciężki, [2]: Atak z blokiem,"
                            " [3]: Strzał z łuku")
                self.atak(o, x)
            if self.ph > 0:
                print("Zwycięstwo!")
                restored_hp = round((3 / 4) * (starting_hp - self.ph))
                self.ph += restored_hp
                print("Przywrócono [{}] pkt. zdrowia".format(restored_hp))
                print("(Zdrowie gracza: [{}])".format(self.ph))
                self.pa += 1
                print("Twój atak wzrósł o [1] pkt.\n")
                return 1
            else:
                print("Porażka!")
                return 0
        except TypeError:
            print("błąd we wprowdzonych danych")
        except:
            print("nieobsługiwany błąd")

    def walka_2(self, o):
        def komunikat():
            tab = ['Tylko na tyle Cię stać..?',
                   'Też mi wyzwanie...',
                   'Walczysz gorzej niż moja babcia...',
                   'To miał być atak..?',
                   'Ha!',
                   '*Niezrozumiałe trąbienie*']
            return tab[r.randint(0, len(tab) - 1)]

        try:
            while self.ph > 0 and o.oh > 0:
                print()
                x = pytanie("[1]: Atak ciężki, [2]: Atak z blokiem,"
                            " [3]: Strzał z łuku")
                print()
                print('SZSZG: ' + komunikat() + '\n')
                self.atak(o, x)
            if self.ph > 0:
                print("Zwycięstwo!")
                return 1
            else:
                print("Porażka!")
                return 0
        except TypeError:
            print("błąd we wprowdzonych danych")
        except:
            print("nieobsługiwany błąd")

    def atak(self, o, kind):
        if kind == "1":
            y = r.randint(5, self.pa)
            z = r.randint(5, o.oa)
            o.oh = o.oh - y
            self.ph = self.ph - z
            if y >= self.pa - 2:
                print("CIOS KRYTYCZNY!")
            print("--Zadano[{}] pkt. obrażeń".format(y))
            print("--Stracono[{}] pkt. zdrowia".format(z))
            print("  (Zdrowie przeciwnika: [{}])".format(o.oh))
            print("  (Zdrowie gracza: [{}])".format(self.ph))
            print()
        elif kind == "2":
            y = r.randint(5, self.pa)
            z = r.randint(5, o.oa)
            a = r.randint(2, y - 1)
            b = r.randint(self.pb, z - 1)
            o.oh = o.oh - (y - a)
            self.ph = self.ph - (z - b)
            print("--Zadano[{}] pkt. obrażeń".format(y - a))
            print("--Stracono[{}] pkt. zdrowia, blok = {}%".format(
                z - b,
                round(100 * b / z, 2)))
            print("  (Zdrowie przeciwnika: [{}])".format(o.oh))
            print("  (Zdrowie gracza: [{}])".format(self.ph))
            print()
        elif kind == "3":
            target_size = 20 - self.pag
            target_low = target_size / 2 - 2
            target_high = target_size / 2 + 2

            c = r.randint(1, target_size)
            y = r.randint(20, 25)
            z = r.randint(5, o.oa)
            self.ph = self.ph - z
            if (c >= target_low) and (c <= target_high):
                o.oh = o.oh - y
                print("--Zadano[{}] pkt. obrażeń".format(y))
            elif c < target_low:
                print("Pudlo, za krótki strzał")
            else:
                print("Pudło, przestrzelono")
            print("--Stracono[{}] pkt. zdrowia".format(z))
            print("  (Zdrowie przeciwnika: [{}])".format(o.oh))
            print("  (Zdrowie gracza: [{}])".format(self.ph))
            print()
        else:
            z = r.randint(4, o.oa - 6)
            self.ph = self.ph - z
            print("Błąd ataku (Wciśnij [1], [2] lub [3])")
            print("--Stracono[{}] pkt. zdrowia".format(z))
            print("  (Zdrowie przeciwnika: [{}])".format(o.oh))
            print("  (Zdrowie gracza: [{}])".format(self.ph))
            print()
