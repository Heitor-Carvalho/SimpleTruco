from enum import IntEnum

class ChalangesAction(IntEnum):
    NO_CHALANGE = 0
    DENIED = 1
    ACCEPT = 2

class RoundStatus:

    ROUND_POINTS = [1, 3, 6, 9, 12]

    def __init__(self):
        self.truco_status_ = ChalangesAction.NO_CHALANGE
        self.truco_status_chalanger = None
        self.winner_player_ = None
        self.central_card_ = 0
        self.team_a_round_score_ = 0
        self.team_b_round_score_ = 0
        self.round_point_ = 1
        self.round_turn_ = 0
        self.team_a_played_cards_ = []
        self.team_b_played_cards_ = []

    def set_truco_status(self, truco_status, player):
        self.truco_status_ = truco_status
        self.truco_status_chalanger = player

    def get_truco_status(self):
        return self.truco_status_, self.truco_status_chalanger

    def set_round_winner(self, player):
        self.winner_player_ = player

    def get_round_winner(self):
        return self.winner_player_

    def set_central_card(self, card):
        self.central_card_ = card

    def get_central_card(self):
        return self.central_card_

    def increment_team_a_round_score(self):
        self.team_a_round_score_+=1

    def get_team_a_round_score(self):
        return self.team_a_round_score_

    def increment_team_b_round_score(self):
        self.team_b_round_score_+=1

    def get_team_b_round_score(self):
        return self.team_b_round_score_

    def increase_round_points(self):
        point_index = RoundStatus.ROUND_POINTS.index(self.round_point_)
        if point_index != len(RoundStatus.ROUND_POINTS)-1:
            self.round_point_ = RoundStatus.ROUND_POINTS[point_index+1]

    def get_round_points(self):
        return self.round_point_

    def increase_round_turn(self):
        self.round_turn_+=1

    def get_round_turn(self):
        return self.round_turn_

    def get_team_a_played_cards(self):
        return self.team_a_played_cards_

    def get_team_b_played_cards(self):
        return self.team_b_played_cards_


class GameStatus:

    def __init__(self):
        self.round_status_ = RoundStatus()
        self.team_a_players_ = []
        self.team_b_players_ = []
        self.team_a_score_ = 0
        self.team_b_score_ = 0

    def get_round_status(self):
        return self.round_status_

    def add_to_team_a(self, player):
        self.team_a_players_.append(player)

    def get_team_a_player(self):
        return self.team_a_players_[0]

    def add_to_team_b(self, player):
        self.team_b_players_.append(player)

    def get_team_b_player(self):
        return self.team_b_players_[0]

    def increment_team_a_game_score(self):
        self.team_a_score_ += self.round_status_.get_round_points()

    def get_team_a_score(self):
        return self.team_a_score_

    def increment_team_b_game_score(self):
        self.team_b_score_ += self.round_status_.get_round_points()

    def get_team_b_score(self):
        return self.team_b_score_

    def increment_player_round_team_score(self, player):
        if player in self.team_a_players_:
            self.round_status_.increment_team_a_round_score()
        elif player in self.team_b_players_:
            self.round_status_.increment_team_b_round_score()

        self.round_status_.set_round_winner(player)
        self.round_status_.increase_round_turn()

    def add_played_card(self, player, card):
        if player in self.team_a_players_:
            self.round_status_.team_a_played_cards_.append(card)
        elif player in self.team_b_players_:
            self.round_status_.team_b_played_cards_.append(card)

    def reset_round_status(self):
        self.round_status_ = RoundStatus()
