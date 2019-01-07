import random as r
import sys

GAME_OVER = "game_over"


def pytanie(prompt):
    try:
        return str(input(prompt + "\n- "))
    except TypeError:
        print("błąd we wprowdzonych danych")
    except:
        print("nieobsługiwany błąd")


def wybor(intro, *args):
    index_desc = [(i, a[0]) for i, a in enumerate(args, 1)]

    index_func = {str(i): a[1] for i, a in enumerate(args, 1)}

    prompt = ", ".join("[{}]- {}".format(i, desc) for i, desc in index_desc)

    print()
    print(intro)
    try:
        while True:
            x = pytanie(prompt)
            if x in index_func:
                func_or_return_value = index_func[x]
                if callable(func_or_return_value):
                    result = func_or_return_value()
                    if result is not None:
                        return result
                else:
                    return func_or_return_value
    except TypeError:
        print("błąd we wprowdzonych danych")
    except:
        print("nieobsługiwany błąd")


def komunikat_o_porazce():
    tab = ['Nawet najlepszym się zdarza...',
           'Raz na wozie, raz pod wozem...',
           'Powróć i zmiażdż swych wrogów!',
           'Co Cię nie zabije, to Cię wzmocni...']
    return tab[r.randint(0, len(tab) - 1)]


def szyfr_1(clue):
    a = r.randint(0, 9)
    b = clue
    c = r.randint(0, 9)
    e = r.randint(0, 9)
    d = round((a + c + e) / 3)

    print("(a[{}],b[?],c[?],d[?],e[{}])".format(a, e) +
          "; b, c, d \u2208 <0; 9>"
          "; d \u2248 (a+c+e)/3")

    for i in range(9):
        print("Liczba pozostałych prób- [{}].".format(9 - i))
        try:
            x = input("b- ")
            y = input("c- ")
            z = input("d- ")
        except TypeError:
            print("błąd we wprowdzonych danych")
        except:
            print("nieobsługiwany błąd")
        if x == str(b) and y == str(c) and z == str(d):
            print("a[{}],b[{}],c[{}],d[{}],e[{}]".format(a, b, c, d, e))
            return 1
        if x == str(b) and y == str(c):
            print("a[{}],b[{}],c[{}],d[?],e[{}]".format(a, b, c, e))
        elif x == str(b) and z == str(d):
            print("a[{}],b[{}],c[?],d[{}],e[{}]".format(a, b, d, e))
        elif y == str(c) and z == str(d):
            print("a[{}],b[?],c[{}],d[{}],e[{}]".format(a, c, d, e))
        elif x == str(b) and y != str(c) and z != str(d):
            print("a[{}],b[{}],c[?],d[?],e[{}]".format(a, b, e))
        elif y == str(c) and x != str(b) and z != str(d):
            print("a[{}],b[?],c[{}],d[?],e[{}]".format(a, c, e))
        elif z == str(d) and x != str(b) and y != str(c):
            print("a[{}],b[?],c[?],d[{}],e[{}]".format(a, d, e))
        else:
            print("a[{}],b[?],c[?],d[?],e[{}]".format(a, e))


def zagadka_1():
    a = r.randint(0, 1)
    if a == 0:
        print("Co to za zwierzę,"
              " które rano chodzi na czterech nogach,"
              " w południe na dwóch,"
              " a wieczorem na trzech?")
        print()
        for i in range(9):
            print("Liczba pozostałych prób - [{}]".format(9 - i))
            x = pytanie("Podaj odpowiedź")
            if str.lower(x) in ('człowiek', 'czlowiek'):
                return 1
            else:
                print('Niepoprawna odpowiedź.')
    if a == 1:
        print("Są dwie siostry."
              " Jedna rodzi drugą, a druga pierwszą."
              " Jak mają na imię?")
        print()
        for i in range(9):
            print("Liczba pozostałych prób - [{}].".format(9 - i))
            x = str.lower(pytanie("Podaj odpowiedź"))
            if 'noc' in x and ('dzien' in x or 'dzień' in x):
                return 1
            else:
                print('Niepoprawna odpowiedź.')
    return 0


def koniec():
    print("Do zobaczenia.")
    sys.exit(0)
