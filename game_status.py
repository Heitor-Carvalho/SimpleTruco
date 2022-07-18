from enum import Enum

class TrucoChallengeStatus:

    def __init__(self):
        self.challenge_status = False
        self.challenge_accepted = False
        self.challenger_player = None
        self.challenged_player = None

class RoundStatus:

    ROUND_POINTS = [1, 3, 6, 9, 12]

    def __init__(self):
        self._truco_status = TrucoChallengeStatus()
        self._winner_player = None
        self._central_card = 0
        self._team_a_round_score_ = 0
        self._team_b_round_score_ = 0
        self._round_point = 1
        self._round_turn = 0
        self._team_a_played_cards = []
        self._team_b_played_cards = []

    def set_truco_status(self, truco_status):
        self._truco_status = truco_status

    def get_truco_status(self):
        return self._truco_status

    def set_round_winner(self, player_name):
        self._winner_player = player_name

    def get_round_winner(self):
        return self._winner_player

    def set_central_card(self, card):
        self._central_card = card

    def get_central_card(self):
        return self._central_card

    def increment_team_a_round_score(self):
        self._team_a_round_score_+=1

    def get_team_a_round_score(self):
        return self._team_a_round_score_

    def increment_team_b_round_score(self):
        self._team_b_round_score_+=1

    def get_team_b_round_score(self):
        return self._team_b_round_score_

    def increase_round_points(self):
        point_index = RoundStatus.ROUND_POINTS.index(self._round_point)
        if point_index != len(RoundStatus.ROUND_POINTS)-1:
            self._round_point = RoundStatus.ROUND_POINTS[point_index+1]

    def get_round_points(self):
        return self._round_point

    def increase_round_turn(self):
        self._round_turn+=1

    def get_round_turn(self):
        return self._round_turn

    def get_team_a_played_cards(self):
        return self._team_a_played_cards

    def get_team_b_played_cards(self):
        return self._team_b_played_cards


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
            self.round_status_._team_a_played_cards.append(card)
        elif player in self.team_b_players_:
            self.round_status_._team_b_played_cards.append(card)

    def reset_round_status(self):
        self.round_status_ = RoundStatus()
