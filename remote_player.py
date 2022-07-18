from player import Player
from game_strategies import DummyStretagy, UserStretagy
from view import ClientConsoleView

if __name__ == "__main__":
    view = ClientConsoleView("127.0.0.1", 4022)
    view.start()
