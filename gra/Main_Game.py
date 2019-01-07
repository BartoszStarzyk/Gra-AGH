from gra import *


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
                koniec()

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
                     ("Nie", koniec))


if __name__ == "__main__":
    game = Game()
    game.start()
