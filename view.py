import os
import math
import itertools

from game_status import ChalangesAction
from truco_events import TrucoEvents

class PrintViewer:

    message_length = 60

    def get_left_pad(self, text):
        left_dots = math.floor((PrintViewer.message_length-len(text))/2)
        return "-"*left_dots

    def get_right_pad(self, text):
        right_dots = math.ceil((PrintViewer.message_length-len(text))/2)
        return "-"*right_dots

    def print_pad(self, text=""):
        if len(text) == 0:
            print(self.get_left_pad(text) + "--" + self.get_right_pad(text))
        else:
            print(self.get_left_pad(text) + " " + text + " " + self.get_right_pad(text))

    def handle_event(self, event, data):
        if event == TrucoEvents.GAME_STARTED:
            self._show_game_status(data["game_status"])
            self._clear_screen(wait=True)
        elif event == TrucoEvents.ROUND_PREPARED:
            self._show_round_status(data["current_player"], data["player_a"], data["player_b"], data["round_status"])
        elif event == TrucoEvents.ROUND_STARTED:
            self._clear_screen(wait=True)
            self._show_round_status(data["current_player"], data["player_a"], data["player_b"], data["round_status"])
        elif event == TrucoEvents.RAN_TRUCO_SESSION:
            self._show_truco_message(data["round_status"])
        elif event == TrucoEvents.ROUND_RESOLVED:
            self._clear_screen()
            self._show_round_status(data["current_player"], data["player_a"], data["player_b"], data["round_status"])
        elif event == TrucoEvents.ROUND_ENDED:
            self._clear_screen(wait=True)
            self._show_round_end(data["player_a"], data["player_b"], data["round_status"])
            self._show_game_status(data["game_status"])
            self._clear_screen(wait=True)
        elif event == TrucoEvents.GAME_ENDED:
            self._show_game_status(data["game_status"])
            self._clear_screen(wait=True)

    def _show_game_status(self, game_status):
        try:
            self.print_pad("Game Score")
            self.print_pad(f"Team {game_status.get_team_a_player().name().ljust(10)} Game Score: {game_status.get_team_a_score()}")
            self.print_pad(f"Team {game_status.get_team_b_player().name().ljust(10)} Game Score: {game_status.get_team_b_score()}")
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def _show_round_status(self, current_player, team_a_player, team_b_player, round_status):
        try:
            self.print_pad(f"Round {round_status.get_round_turn()+1} Status")
            self.print_pad(f"Team {team_a_player.name().ljust(10)} Round Score: {round_status.get_team_a_round_score()}")
            self.print_pad(f"Team {team_b_player.name().ljust(10)} Round Score: {round_status.get_team_b_round_score()}")
            self.print_pad(f"Central Card : {round_status.get_central_card()}")
            self.print_pad(f"Current round points: {round_status.get_round_points()}")
            self.print_pad(f"Current Player: {current_player.name()}")
            print("\n")

            self.print_pad("Played Cards")
            print(f"Cards Played {team_a_player.name()}".ljust(25) + " | " + 
                  f"Cards Played {team_b_player.name()}".ljust(25))
            if len(round_status.get_team_a_played_cards()) == 0 and \
               len(round_status.get_team_b_played_cards()) == 0:
                print(f"?".ljust(25) + " | " + f"?".ljust(25))
            else:
                for card_a, card_b in itertools.zip_longest(round_status.get_team_a_played_cards(),
                                                            round_status.get_team_b_played_cards(),
                                                            fillvalue="?"):
                    print(f"{card_a}".ljust(25) + " | " + f"{card_b}".ljust(25))
            self.print_pad()
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def _show_round_end(self, team_a_player, team_b_player, round_status):
        try:
            self.print_pad("Round ended:")
            print(f"Cards Played {team_a_player.name()}".ljust(25) + " | "\
                  f"Cards Payed {team_b_player.name()}".ljust(25))
            for card_a, card_b in itertools.zip_longest(round_status.get_team_a_played_cards(),
                                                        round_status.get_team_b_played_cards(),
                                                        fillvalue="?"):
                print(f"{card_a}".ljust(25) + " | " + f"{card_b}".ljust(25))
            print(f"Round Winner player: {round_status.get_round_winner().name()}")
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def _show_truco_message(self, round_status):
        try:
            truco_status, player = round_status.get_truco_status()
            if truco_status == ChalangesAction.NO_CHALANGE:
                self.print_pad(f"No truco by {player.name()}")
            elif truco_status == ChalangesAction.ACCEPT:
                self.print_pad(f"Truco Accepted by {player.name()}")
                self.print_pad(f"Round value: {round_status.get_round_points()}")
            else:
                self.print_pad(f"Truco Denied by {player.name()}")
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def _clear_screen(self, wait=False):
        if wait:
            input()
        os.system("clear")

