from view import PrintViewer
from cards import DeckBuilder, Value
from game_status import GameStatus, ChalangesAction
from player import Player, DummyStretagy, UserStretagy, PlayersManager

# TODO Implement other stretagy

class TrucoGame:

    def __init__(self, player_manager, deck_builder, viwer):
        self.player_manager_ = player_manager
        self.deck_builder_ = deck_builder
        self.deck_ = deck_builder.build_truco_deck()
        self.viwer_ = viwer
        self.game_status_ = GameStatus()

    def start(self):
        self.game_status_.add_to_team_a(self.player_manager_.get_current_player())
        self.game_status_.add_to_team_b(self.player_manager_.get_next_player())

        self.viwer_.show_game_status(self.game_status_)
        self.viwer_.clear_screen(wait=True)

        while self._check_game_end() == False:

            self._prepare_rounds()
            self.viwer_.show_round_status(self.player_manager_.get_current_player(), \
                                          self.game_status_.get_team_a_player(),     \
                                          self.game_status_.get_team_b_player(),     \
                                          self.game_status_.get_round_status())

            while not self._check_round_end():
                self._truco_session()
                self.viwer_.show_truco_message(self.game_status_.get_round_status())

                if self._check_round_end():
                    break

                self.viwer_.clear_screen(wait=True)
                self.viwer_.show_round_status(self.player_manager_.get_current_player(), \
                                              self.game_status_.get_team_a_player(),     \
                                              self.game_status_.get_team_b_player(),     \
                                              self.game_status_.get_round_status())

                self._play_cards()
                self.player_manager_.move_next_player()

                self._truco_session()
                self.viwer_.show_truco_message(self.game_status_.get_round_status())

                self._resolve_round()

                self.viwer_.clear_screen()
                self.viwer_.show_round_status(self.player_manager_.get_current_player(), \
                                              self.game_status_.get_team_a_player(),     \
                                              self.game_status_.get_team_b_player(),     \
                                              self.game_status_.get_round_status())

            self._round_end()
            self.player_manager_.move_next_player()

            self.viwer_.clear_screen(wait=True)

            self.viwer_.show_round_end(self.game_status_.get_team_a_player(), \
                                       self.game_status_.get_team_b_player(), \
                                       self.game_status_.get_round_status())
            self.viwer_.show_game_status(self.game_status_)

            self.viwer_.clear_screen(wait=True)


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

    viwer = PrintViewer()
    deck_builder = DeckBuilder()
    players = [Player(UserStretagy(), "Player 1"), Player(UserStretagy(), "Player 2")]
    player_manager = PlayersManager(players)

    truco_game = TrucoGame(player_manager, deck_builder, viwer)
    truco_game.start()

