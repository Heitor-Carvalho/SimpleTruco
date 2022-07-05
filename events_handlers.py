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
        if event == TrucoGame.TrucoGameEvents.GAME_STARTED:
            self._view.show_game_status(game_status)
            self._view.clear_screen()
        elif event == TrucoGame.TrucoGameEvents.ROUND_PREPARED:
            self._view.clear_screen()
            self._view.show_round_status(current_player_name, game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.ROUND_STARTED:
            self._view.clear_screen()
            self._view.show_round_status(current_player_name, game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.RAN_TRUCO_SESSION:
            self._view.show_truco_message(game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.ROUND_RESOLVED:
            self._view.clear_screen()
            self._view.show_round_status(current_player_name, game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
        elif event == TrucoGame.TrucoGameEvents.ROUND_ENDED:
            self._view.clear_screen()
            self._view.show_round_end(game_status.get_team_a_player(), game_status.get_team_b_player(), game_status.get_round_status())
            self._view.show_game_status(game_status)
        elif event == TrucoGame.TrucoGameEvents.GAME_ENDED:
            self._view.show_end_game(game_status)
        else:
            print("Unkwon event")
