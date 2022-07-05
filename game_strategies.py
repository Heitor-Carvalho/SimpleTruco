import time

from abc import ABC, abstractmethod

class GameStrategy(ABC):

    @abstractmethod
    def make_challenge(self, name, cards, game_status):
        pass

    @abstractmethod
    def handle_challenge(self, name, cards, game_status):
        pass

    @abstractmethod
    def ask_press(self):
        pass

    @abstractmethod
    def play_card(self, name, cards, game_status):
        pass

class UserStretagy(GameStrategy):

    def __init__(self, view):
        self._view = view

    def make_challenge(self, name, cards, game_status):
        return self._view.ask_make_challenge(name, cards, game_status)

    def handle_challenge(self, name, cards, game_status):
        return self._view.ask_handle_challenge(name, cards, game_status)

    def ask_press(self):
        self._view.ask_press()

    def play_card(self, name, cards, game_status):
        card_nb = self._view.ask_play_card(name, cards, game_status)
        return cards.pop(card_nb)

class DummyStretagy(GameStrategy):

    TIME = 0.01

    def make_challenge(self, name, cards, game_status):
        time.sleep(DummyStretagy.TIME)
        return False

    def handle_challenge(self, name, cards, game_status):
        time.sleep(DummyStretagy.TIME)
        return True

    def ask_press(self):
        time.sleep(DummyStretagy.TIME*2)
        pass

    def play_card(self, name, cards, game_status):
        time.sleep(DummyStretagy.TIME)
        if len(cards) != 0:
            return cards.pop()
        else:
            print("No cards avaliable")

