import random
from abc import ABC, abstractmethod
from enum import Enum

class PlayersManager:

    def __init__(self, players):
        self._players = players
        self._current_player = self._chose_random_current_player()

    def _chose_random_current_player(self):
        return random.choice(self._players)

    def get_players(self):
        return self._players

    def get_current_player(self):
        return self._current_player

    def get_next_player(self):
        index = self._players.index(self._current_player)
        return self._players[(index + 1) % len(self._players)]

    def move_next_player(self):
        index = self._players.index(self._current_player)
        self._current_player = self._players[(index + 1) % len(self._players)]

class AbstractPlayer(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def handle_cards(self, cards):
        pass

    @abstractmethod
    def clean_cards(self):
        pass

    @abstractmethod
    def make_challenge(self, game_status):
        pass

    @abstractmethod
    def handle_challenge(self, game_status):
        pass

    @abstractmethod
    def ask_press(self):
        pass

    @abstractmethod
    def play_card(self, game_status):
        pass

class Player(AbstractPlayer):

    def __init__(self, strategy, name):
        self._strategy = strategy
        self._cards = []
        self._name = name

    def name(self):
        return self._name

    def handle_cards(self, cards):
        self._cards = cards

    def clean_cards(self):
        self._cards = []

    def make_challenge(self, game_status):
        return self._strategy.make_challenge(self._name, self._cards, game_status)

    def handle_challenge(self, game_status):
        return self._strategy.handle_challenge(self._name, self._cards, game_status)

    def ask_press(self):
        return self._strategy.ask_press()

    def play_card(self, game_status):
        return self._strategy.play_card(self._name, self._cards, game_status)

