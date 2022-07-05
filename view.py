import socket
import pickle
import threading
import os
import math
import itertools

from game_status import ChalangesAction
from abc import ABC, abstractmethod

class View(ABC):

    @abstractmethod
    def ask_press(self):
        pass

    @abstractmethod
    def ask_make_challenge(self, name, cards, game_status):
        pass

    @abstractmethod
    def ask_handle_challenge(self, name, cards, game_status):
        pass

    @abstractmethod
    def ask_play_card(self, name, cards, game_status):
        pass

    @abstractmethod
    def show_game_status(self, game_status):
        pass

    @abstractmethod
    def show_end_game(self, game_status):
        pass

    @abstractmethod
    def show_round_status(self, current_player, team_a_player, team_b_player, round_status):
        pass

    @abstractmethod
    def show_round_end(self, team_a_player, team_b_player, round_status):
        pass

    @abstractmethod
    def show_truco_message(self, round_status):
        pass

    @abstractmethod
    def clear_screen(self, wait):
        pass

class ConsoleView(View):

    message_length = 60

    def ask_press(self):
        input()
        return True

    def ask_make_challenge(self, name, cards, game_status):
        print(f"Current user {name}")

        self._show_hand(cards)
        print("0 - No Truco [default]")
        print("1 - Truco")
        truco = 0
        try:
            truco = int(input("Truco?: "))
        except Exception:
            truco = 0

        return truco == 1

    def ask_handle_challenge(self, name, cards, game_status):
        try:
            print(f"Current user {name}")
        except Exception as e:
            print(f"Error: str(e)")

        self._show_hand(cards)
        print("0 - Accept")
        print("1 - Denied [default]")
        accept = 0
        try:
            accept = int(input("Accept?: "))
        except Exception:
            accept = 1

        return accept == 0

    def ask_play_card(self, name, cards, game_status):
        print(f"Current user {name}")
        card_nb = -1
        while card_nb == -1:
            self._show_hand(cards)
            try:
                card_nb = int(input("Card Number: "))-1
            except Exception:
                pass

        return card_nb

    @staticmethod
    def _show_hand(cards):
        print("Player Hands:")
        for index, card in enumerate(cards):
            print(f"Card {index+1}: {card}")

    def show_game_status(self, game_status):
        try:
            self.print_pad("Game Score")
            self.print_pad(f"Team {game_status.get_team_a_player().ljust(10)} Game Score: {game_status.get_team_a_score()}")
            self.print_pad(f"Team {game_status.get_team_b_player().ljust(10)} Game Score: {game_status.get_team_b_score()}")
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def show_end_game(self, game_status):
        try:
            if game_status.get_team_a_score() > game_status.get_team_b_score():
                player = game_status.get_team_a_player()
            else:
                player = game_status.get_team_b_player()
            self.print_pad()
            self.print_pad(f"Congratulations {player}: You won !!")
            self.print_pad()
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def show_round_status(self, current_player_name, team_a_player, team_b_player, round_status):
        try:
            self.print_pad(f"Round {round_status.get_round_turn()+1} Status")
            self.print_pad(f"Team {team_a_player.ljust(10)} Round Score: {round_status.get_team_a_round_score()}")
            self.print_pad(f"Team {team_b_player.ljust(10)} Round Score: {round_status.get_team_b_round_score()}")
            self.print_pad(f"Central Card : {round_status.get_central_card()}")
            self.print_pad(f"Current round points: {round_status.get_round_points()}")
            self.print_pad(f"Current Player: {current_player_name}")
            print("\n")

            self.print_pad("Played Cards")
            print(f"Cards Played {team_a_player}".ljust(25) + " | " + 
                  f"Cards Played {team_b_player}".ljust(25))
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

    def show_round_end(self, team_a_player, team_b_player, round_status):
        try:
            self.print_pad("Round ended:")
            print(f"Cards Played {team_a_player}".ljust(25) + " | "\
                  f"Cards Payed {team_b_player}".ljust(25))
            for card_a, card_b in itertools.zip_longest(round_status.get_team_a_played_cards(),
                                                        round_status.get_team_b_played_cards(),
                                                        fillvalue="?"):
                print(f"{card_a}".ljust(25) + " | " + f"{card_b}".ljust(25))
            print(f"Round Winner player: {round_status.get_round_winner()}")
            print(f"Points gained: {round_status.get_round_points()}")
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def show_truco_message(self, round_status):
        try:
            truco_status, player = round_status.get_truco_status()
            if truco_status == ChalangesAction.NO_CHALANGE:
                self.print_pad(f"No truco by {player}")
            elif truco_status == ChalangesAction.CHALANGE:
                self.print_pad(f"Truco by {player}")
            elif truco_status == ChalangesAction.ACCEPT:
                self.print_pad(f"Truco Accepted by {player}")
                self.print_pad(f"New round value: {round_status.get_round_points()}")
            elif truco_status == ChalangesAction.DENIED:
                self.print_pad(f"Truco Denied by {player}")
            else:
                pass
        except Exception as e:
            print(f"Message failed: {str(e)}")

    def clear_screen(self, wait=False):
        if wait:
            input()
        os.system("clear")

    def print_pad(self, text=""):
        if len(text) == 0:
            print(self._get_left_pad(text) + "--" + self._get_right_pad(text))
        else:
            print(self._get_left_pad(text) + " " + text + " " + self._get_right_pad(text))

    @staticmethod
    def _get_left_pad(text):
        left_dots = math.floor((ConsoleView.message_length-len(text))/2)
        return "-"*left_dots

    @staticmethod
    def _get_right_pad(text):
        right_dots = math.ceil((ConsoleView.message_length-len(text))/2)
        return "-"*right_dots

class ServerView:

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._socket = None
        self._server_socket = None
        self._stop_running = False

    def start(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self._ip, self._port))
        self._server_socket.listen()
        self._wait_client()

    def finish(self):
        if self._socket:
            self._socket.close()
        self._server_socket.close()

    def ask_press(self):
        return self._ask_client("ask_press", ())

    def ask_make_challenge(self, name, cards, game_status):
        return self._ask_client("ask_make_challenge", (name, cards, game_status))

    def ask_handle_challenge(self, name, cards, game_status):
        return self._ask_client("ask_handle_challenge", (name, cards, game_status))

    def ask_play_card(self, name, cards, game_status):
        return self._ask_client("ask_play_card", (name, cards, game_status))

    def show_game_status(self, game_status):
        return self._ask_client("show_game_status", (game_status,))

    def show_end_game(self, game_status):
        return self._ask_client("show_end_game", (game_status,))

    def show_round_status(self, current_player_name, team_a_player, team_b_player, round_status):
        return self._ask_client("show_round_status", (current_player_name, team_a_player, team_b_player, round_status))

    def show_round_end(self, team_a_player, team_b_player, round_status):
        return self._ask_client("show_round_end", (team_a_player, team_b_player, round_status))

    def show_truco_message(self, round_status):
        return self._ask_client("show_truco_message", (round_status,))

    def clear_screen(self, wait=False):
        return self._ask_client("clear_screen", (wait,))

    def _wait_client(self):
        try:
            print(f"Waiting remote view to connect")
            self._socket, addr = self._server_socket.accept()
            print(f"Remote view connected from {addr}")
            self._server_socket.settimeout(60)
        except Exception as e:
            pass

    def _ask_client(self, action, data):
        send_data = pickle.dumps((action, data))
        if self._socket:
            self._socket.sendall(send_data)
            recv_data = self._socket.recv(2**20)
            if recv_data:
                (action_recv, data_recv) = pickle.loads(recv_data)
                if action_recv == action:
                    return data_recv


class ClientConsoleView(ConsoleView, threading.Thread):

    def __init__(self, server_ip, server_port):
        threading.Thread.__init__(self)
        self._server_ip = server_ip
        self._server_port = server_port
        self._socket = None
        self._stop_running = False

    def start(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self._server_ip, self._server_port))
        threading.Thread.start(self)

    def finish(self):
        self._socket.close()
        self._stop_running = True

    def run(self):
        while not self._stop_running:
            action_data = self._socket.recv(2**20)
            data = True
            if action_data:
                (action, data_recv) = pickle.loads(action_data)
                try:
                    data = getattr(self, action)(*data_recv)
                    send_data = pickle.dumps((action, data))
                    self._socket.sendall(send_data)
                except Exception as e:
                    print(e)


