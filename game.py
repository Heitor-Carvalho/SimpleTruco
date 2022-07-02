from view import PrintViewer
from truco_events import TrucoEvents
from cards import DeckBuilder, Value
from game_status import GameStatus, ChalangesAction
from player import Player, DummyStretagy, UserStretagy, PlayersManager

# TODO Implement other stretagy
class TrucoGame:

    def __init__(self, player_manager, deck_builder, handlers=[]):
        self.player_manager_ = player_manager
        self.deck_builder_ = deck_builder
        self.deck_ = deck_builder.build_truco_deck()
        self.handlers_ = handlers
        self.game_status_ = GameStatus()

    def start(self):
        self.game_status_.add_to_team_a(self.player_manager_.get_current_player())
        self.game_status_.add_to_team_b(self.player_manager_.get_next_player())

        self._emit_event(TrucoEvents.GAME_STARTED)
        while self._check_game_end() == False:

            self._prepare_rounds()
            self._emit_event(TrucoEvents.ROUND_PREPARED)

            while not self._check_round_end():
                self._truco_session()
                self._emit_event(TrucoEvents.RAN_TRUCO_SESSION)

                if self._check_round_end():
                    break

                self._emit_event(TrucoEvents.ROUND_STARTED)

                self._play_cards()
                self.player_manager_.move_next_player()

                self._truco_session()
                self._emit_event(TrucoEvents.RAN_TRUCO_SESSION)

                self._resolve_round()
                self._emit_event(TrucoEvents.ROUND_RESOLVED)

            self._round_end()
            self.player_manager_.move_next_player()
            self._emit_event(TrucoEvents.ROUND_ENDED)

        self._emit_event(TrucoEvents.GAME_ENDED)

    def register_event_listener(self, handler):
        self.handlers_.append(handler)

    def _emit_event(self, event):
        data = self._get_event_data(event)
        for handler in self.handlers_:
            handler.handle_event(event, data)

    def _get_event_data(self, event):
        data = {}
        if event == TrucoEvents.GAME_STARTED:
            data = {"game_status": self.game_status_}
        elif event == TrucoEvents.RAN_TRUCO_SESSION:
            data = {"round_status":     self.game_status_.get_round_status()}
        elif event == TrucoEvents.ROUND_STARTED  or \
             event == TrucoEvents.ROUND_RESOLVED or \
             event == TrucoEvents.ROUND_PREPARED:
            data = {"current_player": self.player_manager_.get_current_player(), \
                    "player_a":       self.game_status_.get_team_a_player(),     \
                    "player_b":       self.game_status_.get_team_b_player(),     \
                    "round_status":   self.game_status_.get_round_status()}
        elif event == TrucoEvents.ROUND_ENDED:
            data = {"current_player: ": self.player_manager_.get_current_player(), \
                    "player_a":         self.game_status_.get_team_a_player(),     \
                    "player_b":         self.game_status_.get_team_b_player(),     \
                    "round_status":     self.game_status_.get_round_status(),      \
                    "game_status":     self.game_status_}
        elif event == TrucoEvents.GAME_ENDED:
            data = {"game_status":     self.game_status_}

        return data

    def _compare_cards(self, central_card, card1, card2):
        if card1.value_.value == (central_card.value_.value+1 % Value.KING) and\
           card2.value_.value == (central_card.value_.value+1 % Value.KING):
            return card1.suit_ < card2.suit_
        if card1.value_.value == (central_card.value_.value+1 % Value.KING):
            return True
        if card2.value_.value == (central_card.value_.value+1 % Value.KING):
            return False

        return card1 > card2

    def _prepare_deck(self):
        self.deck_ = deck_builder.rebuild()
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

    def _truco_session(self):
        while True:
            chalanged = self.player_manager_.get_current_player().make_chalange(self.game_status_)
            if chalanged == False:
                self.game_status_.get_round_status().set_truco_status(ChalangesAction.NO_CHALANGE, self.player_manager_.get_current_player())
                break
            else:
                accept = self.player_manager_.get_next_player().handle_chalange(self.game_status_)
                if accept:
                    self.game_status_.get_round_status().increase_round_points()
                    self.game_status_.get_round_status().set_truco_status(ChalangesAction.ACCEPT, self.player_manager_.get_next_player())
                else:
                    self.game_status_.increment_player_round_team_score(self.player_manager_.get_current_player())
                    self.game_status_.get_round_status().set_truco_status(ChalangesAction.DENIED, self.player_manager_.get_next_player())
                    break

    def _play_cards(self):
        card_current_player = self.player_manager_.get_current_player().play_card(self.game_status_)
        self.game_status_.add_played_card(self.player_manager_.get_current_player(), card_current_player)

    def _round_end(self):
        if self.game_status_.get_round_status().get_team_a_round_score() > \
           self.game_status_.get_round_status().get_team_b_round_score():
           self.game_status_.increment_team_a_game_score()
        else:
           self.game_status_.increment_team_b_game_score()

    def _check_round_end(self):
        truco_status, _ = self.game_status_.get_round_status().get_truco_status()
        return self.game_status_.get_round_status().get_round_turn() == 3   or \
               self.game_status_.get_round_status().get_team_a_round_score() == 2 or \
               self.game_status_.get_round_status().get_team_b_round_score() == 2 or \
               truco_status == ChalangesAction.DENIED

    def _check_game_end(self):
        return self.game_status_.get_team_a_score() >= 12 or \
               self.game_status_.get_team_b_score() >= 12



if __name__ == "__main__":

    viewer = PrintViewer()
    deck_builder = DeckBuilder()

    players = [Player(UserStretagy(), "Player 1"), Player(UserStretagy(), "Player 2")]
    player_manager = PlayersManager(players)

    truco_game = TrucoGame(player_manager, deck_builder)
    truco_game.register_event_listener(viewer)
    truco_game.start()

