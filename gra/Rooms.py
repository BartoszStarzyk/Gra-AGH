from gra.Game_functions import *
from gra.Characters import *


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

    def wejscie(self, _player):
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
                      " Drzwi do kolejnego pokoju stoją otworem."
                      " Co robisz?", 0)

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
                    "Pierwsza zawiera w sobie czerwony płyn, druga"
                    " niebieski.\nCo robisz?",
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
            koniec()

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
