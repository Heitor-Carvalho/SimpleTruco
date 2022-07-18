import pytest

from cards import TrucoCard
from game_status import GameStatus, RoundStatus, TrucoChallengeStatus

@pytest.fixture
def create_truco_status():
    return RoundStatus()

@pytest.fixture
def create_game_status():
    return GameStatus()

def test_round_status_truco_status(create_truco_status):
    round_status = create_truco_status

    truco_status = TrucoChallengeStatus()
    truco_status.challenge_status = True
    truco_status.challenge_accepted = True
    truco_status.challenger_player = "P1Test"
    truco_status.challenged_player = "P2Test"

    round_status.set_truco_status(truco_status)

    truco_status_get = round_status.get_truco_status()
    assert truco_status_get.challenge_status == True
    assert truco_status_get.challenge_accepted == True
    assert truco_status_get.challenger_player == "P1Test"
    assert truco_status_get.challenged_player == "P2Test"

@pytest.mark.parametrize("player", ["p1", "p2"])
def test_round_status_round_winner(create_truco_status, player):
    round_status = create_truco_status
    round_status.set_round_winner(player)
    player_get = round_status.get_round_winner()
    assert player_get == player_get

@pytest.mark.parametrize("card", [TrucoCard(1, 1), TrucoCard(10, 3)])
def test_round_status_get_central_card(create_truco_status, card):
    round_status = create_truco_status
    round_status.set_central_card(card)
    card_get = round_status.get_central_card()
    assert card_get == card_get

def test_round_status_round_score_teams(create_truco_status):
    round_status = create_truco_status
    assert round_status.get_team_a_round_score() == 0
    round_status.increment_team_a_round_score()
    assert round_status.get_team_a_round_score() == 1
    round_status.increment_team_a_round_score()
    assert round_status.get_team_a_round_score() == 2
    card_get = round_status.get_central_card()
    assert round_status.get_team_b_round_score() == 0
    round_status.increment_team_b_round_score()
    assert round_status.get_team_b_round_score() == 1
    round_status.increment_team_b_round_score()
    assert round_status.get_team_b_round_score() == 2

def test_round_status_increment_round_score(create_truco_status):
    round_status = create_truco_status
    assert round_status.get_round_points() == 1
    round_status.increase_round_points()
    assert round_status.get_round_points() == 3
    round_status.increase_round_points()
    assert round_status.get_round_points() == 6
    round_status.increase_round_points()
    assert round_status.get_round_points() == 9
    round_status.increase_round_points()
    assert round_status.get_round_points() == 12
    round_status.increase_round_points()
    assert round_status.get_round_points() == 12

def test_round_status_increase_round_turn(create_truco_status):
    round_status = create_truco_status
    round_status.increase_round_turn()
    assert round_status.get_round_turn() == 1
    round_status.increase_round_turn()
    assert round_status.get_round_turn() == 2
    round_status.increase_round_turn()
    assert round_status.get_round_turn() == 3

def test_game_status_get_round_status(create_game_status):
    game_status = create_game_status
    assert isinstance(game_status.get_round_status(), RoundStatus)

def test_game_status_increment_teams_score(create_game_status):
    game_status = create_game_status
    assert game_status.get_team_a_score() == 0
    game_status.increment_team_a_game_score()
    assert game_status.get_team_a_score() == 1

    assert game_status.get_team_b_score() == 0
    game_status.increment_team_b_game_score()
    assert game_status.get_team_b_score() == 1

    game_status.get_round_status().increase_round_points()

    game_status.increment_team_a_game_score()
    assert game_status.get_team_a_score() == 4
    game_status.increment_team_b_game_score()
    assert game_status.get_team_b_score() == 4

def test_game_status_increment_player_round_team_score(create_game_status):
    game_status = create_game_status

    class FakePlayer:

        def __init__(self, name):
            self._name = name

        def name(self):
            return self._name

    pa = FakePlayer("A")
    pb = FakePlayer("B")
    game_status.add_to_team_a(pa)
    game_status.add_to_team_b(pb)

    assert game_status.get_team_a_score() == 0
    assert game_status.get_team_b_score() == 0

    game_status.increment_player_round_team_score(pa)
    assert game_status.get_round_status().get_team_a_round_score() == 1

    game_status.increment_player_round_team_score(pb)
    assert game_status.get_round_status().get_team_a_round_score() == 1

def test_game_status_reset_round_status(create_game_status):
    game_status = create_game_status

    round_status_get = game_status.get_round_status()
    round_status_get.increase_round_points()

    assert game_status.get_round_status() == round_status_get

    game_status.reset_round_status()
    assert game_status.get_round_status() != round_status_get


