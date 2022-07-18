import pytest
from mock import Mock

from player import AbstractPlayer, Player
from game_strategies import GameStrategy

from game_status import GameStatus
from cards import TrucoCard

@pytest.fixture
def game_status():
    return GameStatus()

@pytest.fixture
def player_hand():
    return [TrucoCard(1, 1), TrucoCard(10, 2), TrucoCard(4, 3)]

@pytest.mark.parametrize("challenge, handle_challenge", [(False, False), (True, True), (True, False), (False, True)])
def test_player(game_status, player_hand, challenge, handle_challenge):

    mock_stretagy = Mock(GameStrategy)

    player = Player(mock_stretagy, "PTest")

    assert player.name() == "PTest"

    player.handle_cards(player_hand)
    assert player._cards == player_hand

    player.clean_cards()
    assert player._cards == []

    mock_stretagy.ask_press.return_value = None
    mock_stretagy.make_challenge.return_value = challenge
    mock_stretagy.handle_challenge.return_value = handle_challenge
    mock_stretagy.play_card.return_value = player_hand[0]

    assert player.handle_challenge(game_status) == handle_challenge
    assert player.make_challenge(game_status) == challenge
    assert player.ask_press() is None
    assert player.play_card(game_status) == player_hand[0]

