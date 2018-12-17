import random as r
import sys

GAME_OVER = "game_over"


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
        x = input("b- ")
        y = input("c- ")
        z = input("d- ")
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


def pytanie(prompt):
    return str(input(prompt + "\n- "))


def wybor(intro, *args):
    index_desc = [(i, a[0]) for i, a in enumerate(args, 1)]

    index_func = {str(i): a[1] for i, a in enumerate(args, 1)}

    prompt = ", ".join("[{}]- {}".format(i, desc) for i, desc in index_desc)

    print()
    print(intro)
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

    def walka_2(self, o):
        def komunikat():
            tab = ['Tylko na tyle Cię stać..?',
                   'Też mi wyzwanie...',
                   'Walczysz gorzej niż moja babcia...',
                   'To miał być atak..?',
                   'Ha!',
                   '*Niezrozumiałe trąbienie*']
            return tab[r.randint(0, len(tab) - 1)]

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


class Room:
    def __init__(self, name, description, actions_taken):
        self.name = name
        self.description = description
        self.actions_taken = actions_taken


class Room1(Room):
    def __init__(self):
        Room.__init__(self, "1",
                      "Znajdujesz się na dziedzińcu."
                      " Przed sobą widzisz dwa wejścia. Co robisz?", 0)

    def wejscie(self, player):
        if self.actions_taken == 1:
            return wybor(
                self.description,
                ('Idę w prawo', '2R'),
                ('Idę w lewo', '2L'),
            )
        if self.actions_taken == 0:
            self.actions_taken = 1
            return wybor(
                "Twoja rodzina została zamordowana przez pana na tym zamku."
                " Twoim zadaniem jest ją pomścić. \n \n" +
                self.description,
                ('Idę w prawo', '2R'),
                ('Idę w lewo', '2L'),
            )


class Room2L(Room):
    def __init__(self):
        Room.__init__(self, "2L",
                      "Drogi naprzód strzegą zamknięte drzwi. Co robisz?", 0)

    def wejscie(self, player):
        def _wywazam():
            chance = r.randint(0, 1)
            if chance == 0:
                print("To nie był najlepszy pomysł. Zginąłeś.")
                print(komunikat_o_porazce())
                return GAME_OVER
            else:
                self.actions_taken = 2
                player.ph -= 10
                print("Udało Ci się. Straciłes 10 pkt. zdrowia.")
                print('Zdrowie gracza - [{}]'.format(player.ph))
                return "3"

        def _rozgladam():
            if self.actions_taken == 0:
                return wybor(
                    "Na podłodze w narożniku pomieszczenia znajdujesz klucz."
                    " Do czego może słuzyć..? Co robisz?",
                    ('Podnoszę go i próbuję otworzyć drzwi',
                     _podnosze_i_otwieram),
                    ('Wracam', '1')
                )
            if self.actions_taken == 1:
                return wybor("Pomieszczenie jest puste.",
                             ('Idę dalej', '3'),
                             ('Wracam', '1')
                             )
            if self.actions_taken == 2:
                return wybor(
                    "Na podłodze w narożniku pomieszczenia znajdujesz klucz."
                    " Nie zdaje się mieć wielu zastosowań... Co robisz?",
                    ('Podnoszę go i idę dalej', '3'),
                    ('Idę dalej', '3'),
                    ('Wracam ', '1')
                )

        def _podnosze_i_otwieram():
            print("Cóż za pokaz błyskotliwości.")
            self.actions_taken = 1
            return '3'

        if self.actions_taken == 0:
            return wybor(
                self.description,
                ('Rozglądam się po pomieszczeniu', _rozgladam),
                ('Próbuję wywazyć drzwi głową', _wywazam),
                ('Wracam', '1')
            )
        if self.actions_taken == 1 or self.actions_taken == 2:
            return wybor(
                "Drzwi stoją otworem. Co robisz?",
                ('Rozglądam się po pomieszczeniu', _rozgladam),
                ('Wracam', '1'),
            )


class Room2R(Room):
    def __init__(self):
        Room.__init__(self, "2R",
                      "Drogę naprzód zagradza Ci strażnik."
                      " Zdaje się Cię jednak nie dostrzegać."
                      " Co robisz?", 0)

    def wejscie(self, player):
        def _walka():
            print("Do ataku!")
            opponent = Opponent(13, 100)
            if player.walka_1(opponent) == 1:
                self.actions_taken = 1
                return _co_dalej()
            else:
                print(komunikat_o_porazce())
                return GAME_OVER

        def _co_dalej():
            return wybor("Co dalej?",
                         ('Rozglądam się po pomieszczeniu', _nic_ciekawego),
                         ('Idę naprzód', '3'),
                         ('Wracam', '1')
                         )

        def _nic_ciekawego():
            return wybor("Nic ciekawego... Oprócz trupa na podłodze."
                         " Co dalej?",
                         ('Przeszukuję ciało', _nic_ciekawego1),
                         ('Idę naprzód', '3'),
                         ('Wracam', '1')
                         )

        def _nic_ciekawego1():
            return wybor("Wciąż nic ciekawego...",
                         ('Idę naprzód', '3'),
                         ('Wracam', '1')
                         )

        if self.actions_taken == 1:
            return _co_dalej()
        else:
            return wybor(
                self.description,
                ("Walczę", _walka),
                ("Wracam", '1')
            )


class Room3(Room):
    def __init__(self):
        Room.__init__(self, "3",
                      "Znajdujesz się w zbrojowni."
                      " Pomieszczenie wydaje się być puste."
                      " Drzwi do kolejnego pokoju stoją otworem. Co robisz?", 0)

    def wejscie(self, player):
        Room2L.from_room = 3
        Room2R.from_room = 3
        if self.actions_taken == 0:
            clue = r.randint(0, 9)

        def _rozgladam():
            if self.actions_taken == 0:
                return _zamknieta_skrzynia()
            elif self.actions_taken == 1:
                return _otwarta_skrzynia()
            elif self.actions_taken == 2:
                return _pusta_skrzynia()
            elif self.actions_taken == 3:
                return _zamknieta_skrzynia()

        def _zamknieta_skrzynia():
            return wybor(
                "Znajdujesz okutą stalą skrzynię. Dostępu broni zamek"
                " z szyfrem. Co robisz?",
                ('Przeprowadzam dalszą inspekcję pomieszczenia', _papier),
                ('Próbuję otworzyć skrzynię', _otwieram_skrzynie),
                ('Idę dalej', "4"),
                ('Wracam', _wracam)
            )

        def _papier():
            return wybor(
                "Znajdujesz skrawek papieru z napisem '{}'. Co robisz?".format(
                    clue),
                ('Wracam do skrzyni', _rozgladam),
                ('Idę dalej', "4"),
                ('Wracam', _wracam)
            )

        def _otwieram_skrzynie():
            if szyfr_1(clue) == 1:
                self.actions_taken = 1
            else:
                self.actions_taken = 3
            return _rozgladam()

        def _otwarta_skrzynia():
            return wybor(
                "W skrzyni znajdujesz bogato zdobiony miecz."
                " Jakość wykonania jest zadziwiąjąca. Co robisz?",
                ("Podnoszę miecz", _biore_miecz),
                ("Idę dalej", "4"),
                ("Wracam", _wracam)
            )

        def _biore_miecz():
            player.pa += 2
            print("Twój atak wzrósł o 2 pkt.")
            print('Atak gracza - [{}]'.format(player.pa))
            self.actions_taken = 2
            return _rozgladam()

        def _pusta_skrzynia():
            return wybor(
                "Skrzynia jest pusta. Co robisz?",
                ("Idę dalej", "4"),
                ("Wracam", _wracam)
            )

        def _wracam():
            return wybor(
                "Do pomieszczenia po prawej czy po lewej?",
                ('Po prawej', "2R"),
                ('Po lewej', "2L")
            )

        return wybor(
            self.description,
            ('Rozglądam się po pomieszczeniu', _rozgladam),
            ('Idę dalej', "4"),
            ('Wracam', _wracam)
        )


class Room4(Room):
    def __init__(self):
        Room.__init__(self, "4",
                      "Znajdujesz się u stóp wieży."
                      " Dostępu do schodów broni strażnik. Co robisz?",
                      0)

    def wejscie(self, player):
        def walka():
            opponent = Opponent(14, 100)
            print("Do ataku!")
            if player.walka_1(opponent) == 1:
                self.actions_taken = 1
                return co_dalej()
            else:
                print(komunikat_o_porazce())
                return GAME_OVER

        def przeszukanie():
            if self.actions_taken == 1:
                return wybor(
                    "W kieszeni zbroi strażnika znajdujesz dwie fiolki.\n"
                    "Pierwsza zawiera w sobie czerwony płyn, druga niebieski.\n"
                    "Co robisz?",
                    ('Wypijam zawartość "czerwonej fiolki"', fiolka1),
                    ('Wypijam zawartość "niebieskiej fiolki"', fiolka2),
                    ('Wypijam zawartość obu fiolek', fiolka1_2),
                    ('Idę dalej', '5'),
                    ('Wracam', '3')
                )
            if self.actions_taken == 2:
                return wybor("W kieszeni zbroi strażnika znajdujesz fiolkę"
                             " z niebieskim płynem. Co robisz?",
                             ('Wypijam zawartość fiolki"', fiolka1_2),
                             ('Idę dalej', '5'),
                             ('Wracam', '3')
                             )
            if self.actions_taken == 3:
                return wybor("W kieszeni zbroi strażnika znajdujesz fiolkę"
                             " z czerwonym płynem. Co robisz?",
                             ('Wypijam zawartość fiolki"', fiolka1_2),
                             ('Idę dalej', '5'),
                             ('Wracam', '3')
                             )
            if self.actions_taken == 4:
                return wybor("Brak łupów... Co robisz?",
                             ('Idę dalej', '5'),
                             ('Wracam', '3')
                             )

        def co_dalej():
            return wybor(
                'Na podłodze leży ciało strażnika. '
                'Co robisz?',
                ('Przeszukuję ciało', przeszukanie),
                ('Idę dalej', '5'),
                ('Wracam', '3')
            )

        def fiolka1():
            player.ph += 15
            print('To musiała być mikstura zdrowia.\n'
                  'Twoje zdrowie wzrosło o 15 pkt.')
            print('Zdrowie gracza - [{}]'.format(player.ph))
            self.actions_taken = 2
            return wybor('Co dalej?',
                         ('Wypijam zawartość drugiej fiolki', fiolka1_2),
                         ('Idę dalej', '5'),
                         ('Wracam', '3')
                         )

        def fiolka2():
            player.pb += 1
            print('To musiala być mikstura siły.\n'
                  'Twój blok wzrósł o 1 pkt.')
            print('Blok gracza - [{}]'.format(player.pb))
            self.actions_taken = 3
            return wybor('Co dalej?',
                         ('Wypijam zawartość drugiej fiolki', fiolka1_2),
                         ('Idę dalej', '5'),
                         ('Wracam', '3')
                         )

        def fiolka1_2():
            if self.actions_taken == 1:
                return _pije(10, 1)
            elif self.actions_taken == 2:
                return _pije(25, 1)
            elif self.actions_taken == 3:
                return _pije(10, 2)

        def _pije(ph, pb):
            player.ph -= ph
            player.pb -= pb
            print('To nie mogło być najlepsze połączenie.\n'
                  'Twoje zdrowie zmalało o {} pkt.\n'
                  'Twój blok zmalał o {} pkt.'.format(ph, pb))
            print('Zdrowie gracza - [{}]\n blok gracza - [{}]'.format(
                player.ph, player.pb))
            self.actions_taken = 4
            return wybor('Co dalej?',
                         ('Idę dalej', '5'),
                         ('Wracam', '3')
                         )

        if self.actions_taken == 0:
            return wybor(
                self.description,
                ('Walczę', walka),
                ('Wracam', '3')
            )
        else:
            return co_dalej()


class Room5(Room):
    def __init__(self):
        Room.__init__(self, "5",
                      'Przed wejściem do sali tronowej spotykasz sfinksa.'
                      ' Mówi, że zgodzi się Cię przepuścić jeśli poprawnie'
                      ' odpowiesz na jego zagadkę. Co robisz?', 0)

    def wejscie(self, player):
        prebattle_ph = player.ph

        def proba_walki():
            x = str(input("[1]- Atak ciężki, [2]- Atak z blokiem,"
                          " [3]- Strzał z łuku\n-"))
            print("CIOS KRYTYCZNY!\n"
                  "--Zadano[1] pkt. obrazeń")
            lost_ph = player.ph - 1
            if x == '2':
                print("--Stracono[{}] pkt. zdrowia, blok = 0%".format(lost_ph))
            else:
                print("--Stracono[{}] pkt. zdrowia".format(lost_ph))
            print("  (Zdrowie przeciwnika: [999])")
            print("  (Zdrowie gracza: [1])")
            print()
            player.ph = 1
            self.actions_taken = 1
            return wybor('Widziałem efektywniejsze próby.\n'
                         'Kontynuować walkę?',
                         ('Tak', game_over),
                         ('Nie', co_dalej_1)
                         )

        def zagadka():
            odpowiedz = zagadka_1()
            if odpowiedz == 1 and self.actions_taken == 1:
                player.ph = prebattle_ph
                print('Sfinks ustępuje Ci z drogi.')
                print('Przywrócono [{}] pkt. zdrowia'.format(prebattle_ph - 1))
                print('Zdrowie gracza [{}]'.format(player.ph))
                self.actions_taken = 2
                return co_dalej_2()

            elif odpowiedz == 1:
                print('Sfinks ustępuje Ci z drogi.')
                self.actions_taken = 2
                return co_dalej_2()

            else:
                print('Porażka')
                print(komunikat_o_porazce())
                return GAME_OVER

        def co_dalej_1():
            return wybor('Co dalej?',
                         ('Podejmuję wyzwanie', zagadka),
                         ('Wracam', '4')
                         )

        def co_dalej_2():
            return wybor('Stoisz przed wejściem do sali tronowej. Co robisz?',
                         ('Wchodzę do środka', '6'),
                         ('Wracam', '4')
                         )

        def game_over():
            print(komunikat_o_porazce())
            return GAME_OVER

        if self.actions_taken == 0:
            return wybor(self.description,
                         ('Podejmuję wyzwanie', zagadka),
                         ('Próbuję walki', proba_walki),
                         ('Wracam', '4')
                         )
        elif self.actions_taken == 1:
            return co_dalej_1()
        else:
            return co_dalej_2()


class Room6(Room):
    def __init__(self):
        Room.__init__(self, '6',
                      'Znajdujesz się w sali tronowej. Na tronie siedzi'
                      ' morderca Twojej rodziny. Słoń Z Serem Zamiast Głowy.\n'
                      'Wszystko wskazuje na to, że Cię poznał. Co robisz?', 0)

    def wejscie(self, player):
        def walka_z_bossem():
            opponent = Opponent(15, 125)
            print("Do ataku!")
            if player.walka_2(opponent) == 1:
                return zwyciestwo()
            else:
                return game_over1()

        def game_over():
            print('Potykasz się na schodach i łamiesz kręgosłup w [15]'
                  ' miejscach. Zdrowie gracza - [-1] pkt.')
            return GAME_OVER

        def game_over1():
            print(komunikat_o_porazce())
            return GAME_OVER

        def zwyciestwo1():
            print('Gratulacje, wygrałeś grę. '
                  'Możesz być z siebie dumny - '
                  '99,9% graczy się to nie udaje.')
            game.koniec()

        def przegrana():
            print('Porażka.')
            return GAME_OVER

        def zwyciestwo():
            return wybor('U twoich stóp leży sterta startego sera.'
                         ' Zemsta została dokonana.'
                         ' Co robisz?',
                         ('Wygrywam grę', przegrana),
                         ('Przegrywam grę', zwyciestwo1)
                         )

        return wybor(self.description,
                     ('Walczę', walka_z_bossem),
                     ('Uciekam z przerażeniem', game_over)
                     )


class Game:
    def __init__(self):
        self.player = None
        self.rooms = [Room1(), Room2L(), Room2R(),
                      Room3(), Room4(), Room5(), Room6()]

    def uruchom(self):
        self.player = self.pokoj_startowy()

        next_room_name = "1"

        while True:
            room = self.znajdz_pokoj(next_room_name)
            next_room_name = room.wejscie(self.player)
            if next_room_name == GAME_OVER:
                return self.zagraj_ponownie()

    def znajdz_pokoj(self, name):
        return {room.name: room for room in self.rooms}[name]

    def start(self):
        print("Witamy w grze!\n")

        while True:
            x = pytanie("Wciśnij [1] aby rozpocząć, [2] aby zakończyć:")
            if x == "1":
                self.uruchom()
                break
            if x == "2":
                self.koniec()

    def pokoj_startowy(self):
        name = pytanie("Podaj swoje imię: ")

        def _wojownik():
            return Player(15, 2, 10, 100, name)

        def _tarczownik():
            return Player(13, 3, 10, 100, name)

        def _strzelec():
            return Player(13, 2, 15, 100, name)

        return wybor("Wybierz klasę",
                     ("Wojownik", _wojownik),
                     ("Tarczownik", _tarczownik),
                     ("Strzelec", _strzelec)
                     )

    def zagraj_ponownie(self):
        def _graj():
            print("Witamy ponownie.")
            new_game = Game()
            new_game.uruchom()

        return wybor("Grasz ponownie?",
                     ("Tak", _graj),
                     ("Nie", self.koniec))

    def koniec(self):
        print("Do zobaczenia.")
        sys.exit(0)


if __name__ == "__main__":
    game = Game()
    game.start()
