from enum import Enum

from game_status import GameStatus, ChalangesAction
from cards import Value

class TrucoGame:

    class TrucoGameEvents(Enum):
        GAME_STARTED      = 0
        ROUND_STARTED     = 1
        ROUND_PREPARED    = 2
        RAN_TRUCO_SESSION = 3
        ROUND_RESOLVED    = 4
        ROUND_ENDED       = 5
        GAME_ENDED        = 6

    def __init__(self, player_manager, deck_builder, handlers=[]):
        self.player_manager_ = player_manager
        self._deck_builder = deck_builder
        self.deck_ = self._deck_builder.build_truco_deck()
        self.handlers_ = handlers
        self.game_status_ = GameStatus()

    def start(self):
        pass

    def run(self):
        self.game_status_.add_to_team_a(self.player_manager_.get_current_player().name())
        self.game_status_.add_to_team_b(self.player_manager_.get_next_player().name())

        self._emit_event(TrucoGame.TrucoGameEvents.GAME_STARTED)
        self.player_manager_.get_current_player().ask_press()
        self.player_manager_.get_next_player().ask_press()
        while not self._check_game_end():

            self._prepare_rounds()
            self._emit_event(TrucoGame.TrucoGameEvents.ROUND_PREPARED)

            while not self._check_round_end():
                self._emit_event(TrucoGame.TrucoGameEvents.ROUND_STARTED)
                self.player_manager_.get_current_player().ask_press()

                while True:
                    challenged_ask = self._ask_challenge()
                    self._emit_event(TrucoGame.TrucoGameEvents.RAN_TRUCO_SESSION)
                    if not challenged_ask:
                        break

                    challenged_accepted = self._accept_challenge()
                    self._emit_event(TrucoGame.TrucoGameEvents.RAN_TRUCO_SESSION)
                    if not challenged_accepted:
                        break

                self.player_manager_.get_current_player().ask_press()

                if self._check_round_end():
                    break

                self._play_cards()
                self.player_manager_.move_next_player()

                self._resolve_round()
                self._emit_event(TrucoGame.TrucoGameEvents.ROUND_RESOLVED)

            self._round_end()
            self.player_manager_.get_current_player().ask_press()
            self.player_manager_.move_next_player()
            self._emit_event(TrucoGame.TrucoGameEvents.ROUND_ENDED)
            self.player_manager_.get_current_player().ask_press()
            self.player_manager_.get_next_player().ask_press()

        self._emit_event(TrucoGame.TrucoGameEvents.GAME_ENDED)
        self.player_manager_.get_current_player().ask_press()
        self.player_manager_.get_next_player().ask_press()

    def finish(self):
        pass

    def register_event_listener(self, handler):
        self.handlers_.append(handler)

    def _emit_event(self, event):
        data = (self.player_manager_.get_current_player().name(), self.game_status_)
        for handler in self.handlers_:
            handler.handle_event(event, data)

    @staticmethod
    def _compare_cards(central_card, card1, card2):
        if card1.value_.value == (central_card.value_.value + 1 % Value.KING) and \
                card2.value_.value == (central_card.value_.value + 1 % Value.KING):
            return card1.suit_ < card2.suit_
        if card1.value_.value == (central_card.value_.value + 1 % Value.KING):
            return True
        if card2.value_.value == (central_card.value_.value + 1 % Value.KING):
            return False

        return card1 > card2

    def _prepare_deck(self):
        self.deck_ = self._deck_builder.rebuild()
        self.deck_.shuffle()
        self.game_status_.get_round_status().set_central_card(self.deck_.get_n_cards(1)[0])

    def _handle_players_cards(self):
        for player in self.player_manager_.get_players():
            player.clean_cards()
            player.handle_cards(self.deck_.get_n_cards(3))

    def _prepare_rounds(self):
        self.game_status_.reset_round_status()
        self._prepare_deck()

        current_player = self.player_manager_.get_current_player()

        self._handle_players_cards()

    def _resolve_round(self):
        if len(self.game_status_.get_round_status().get_team_a_played_cards()) != \
                len(self.game_status_.get_round_status().get_team_b_played_cards()):
            pass
        else:
            if self._compare_cards(self.game_status_.get_round_status().get_central_card(),
                                   self.game_status_.get_round_status().get_team_a_played_cards()[-1],
                                   self.game_status_.get_round_status().get_team_b_played_cards()[-1]):
                self.game_status_.get_round_status().increment_team_a_round_score()
                self.game_status_.get_round_status().set_round_winner(self.game_status_.get_team_a_player())
            else:
                self.game_status_.get_round_status().increment_team_b_round_score()
                self.game_status_.get_round_status().set_round_winner(self.game_status_.get_team_b_player())

            self.game_status_.get_round_status().increase_round_turn()

    def _ask_challenge(self):
        challenged = self.player_manager_.get_current_player().make_challenge(self.game_status_)
        if not challenged:
            self.game_status_.get_round_status().set_truco_status(ChalangesAction.NO_CHALANGE,
                                                                  self.player_manager_.get_current_player().name())
            return False
        else:
            self.game_status_.get_round_status().set_truco_status(ChalangesAction.CHALANGE,
                                                                  self.player_manager_.get_current_player().name())
            return True

    def _accept_challenge(self):
        accept = self.player_manager_.get_next_player().handle_challenge(self.game_status_)
        if accept:
            self.game_status_.get_round_status().increase_round_points()
            self.game_status_.get_round_status().set_truco_status(ChalangesAction.ACCEPT,
                                                                  self.player_manager_.get_next_player().name())
            return True
        else:
            self.game_status_.increment_player_round_team_score(self.player_manager_.get_current_player())
            self.game_status_.get_round_status().set_truco_status(ChalangesAction.DENIED,
                                                                  self.player_manager_.get_next_player().name())
            return False

    def _play_cards(self):
        card_current_player = self.player_manager_.get_current_player().play_card(self.game_status_)
        self.game_status_.add_played_card(self.player_manager_.get_current_player().name(), card_current_player)

    def _round_end(self):
        if self.game_status_.get_round_status().get_team_a_round_score() > \
                self.game_status_.get_round_status().get_team_b_round_score():
            self.game_status_.increment_team_a_game_score()
        else:
            self.game_status_.increment_team_b_game_score()

    def _check_round_end(self):
        truco_status, _ = self.game_status_.get_round_status().get_truco_status()
        # TODO replace magic numbers
        return self.game_status_.get_round_status().get_round_turn() == 3 or \
               self.game_status_.get_round_status().get_team_a_round_score() == 2 or \
               self.game_status_.get_round_status().get_team_b_round_score() == 2 or \
               truco_status == ChalangesAction.DENIED

    def _check_game_end(self):
        return self.game_status_.get_team_a_score() >= 12 or \
               self.game_status_.get_team_b_score() >= 12

