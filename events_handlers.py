from abc import ABC, abstractmethod
from view import ConsoleView
from game import TrucoGame

class EventHandler(ABC):

    @abstractmethod
    def handle_event(self, event, data):
        pass

class ConsoleViewDisplay(EventHandler):

    def __init__(self, view):
        self._view = view

    def handle_event(self, event, data):
        (current_player_name, game_status) = data
        if event == TrucoGame.TrucoGameEvents.STATE_GAME_INIT:
            self._view.show_game_status(game_status)
        elif event == TrucoGame.TrucoGameEvents.STATE_ROUNDS_PREPARE:
            pass
        elif event == TrucoGame.TrucoGameEvents.STATE_ROUND_START:
            self._view.show_round_status(current_player_name, game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.STATE_ROUND_TRUCO_CHALLENGE:
            self._view.show_truco_chalange_message(game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.STATE_ROUND_TRUCO_ACCEPT:
            self._view.show_truco_accept_message(game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.STATE_ROUND_RESOLVE:
            self._view.show_round_status(current_player_name, game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.STATE_ROUNDS_END:
            self._view.show_round_end(game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
            self._view.show_game_status(game_status)
        elif event == TrucoGame.TrucoGameEvents.STATE_GAME_END:
            self._view.show_end_game(game_status)
        else:
            print("Unkwon event")
