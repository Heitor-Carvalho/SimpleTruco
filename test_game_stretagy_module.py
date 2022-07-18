import pytest
from mock import Mock

from game_status import GameStatus
from cards import TrucoCard
from view import View
from game_strategies import DummyStretagy, UserStretagy

@pytest.fixture
def game_status():
    return GameStatus()

@pytest.fixture
def player_hand():
    return [TrucoCard(1, 1), TrucoCard(10, 2), TrucoCard(4, 3)]

@pytest.mark.parametrize("challenge, handle_challenge", [(False, False), (True, True), (True, False), (False, True)])
def test_dummy_stretagy(game_status, player_hand, challenge, handle_challenge):

    DummyStretagy.TIME = 0.01
    dummy_player = DummyStretagy(challenge, handle_challenge)
    assert dummy_player.make_challenge("Ptest", player_hand, game_status) == challenge
    assert dummy_player.handle_challenge("Ptest", player_hand, game_status) == handle_challenge
    assert dummy_player.ask_press() is None
    assert dummy_player.play_card("Ptest", player_hand.copy(), game_status) == player_hand[-1]

    dummy_player.play_card("Ptest", player_hand, game_status)
    assert len(player_hand) == 2

    with pytest.raises(IndexError):
        dummy_player.play_card("Ptest", [], game_status)

@pytest.mark.parametrize("challenge, handle_challenge", [(False, False), (True, True), (True, False), (False, True)])
def test_user_stretagy(game_status, player_hand, challenge, handle_challenge):

    mock_view = Mock(View)
    user_player = UserStretagy(mock_view)

    mock_view.ask_make_challenge.return_value = challenge
    mock_view.ask_handle_challenge.return_value = handle_challenge
    mock_view.ask_play_card.return_value = -1

    assert user_player.make_challenge("Ptest", player_hand, game_status) == challenge
    assert user_player.handle_challenge("Ptest", player_hand, game_status) == handle_challenge
    assert user_player.ask_press() is None
    assert user_player.play_card("Ptest", player_hand.copy(), game_status) == player_hand[-1]

    user_player.play_card("Ptest", player_hand, game_status)
    assert len(player_hand) == 2

    with pytest.raises(IndexError):
        user_player.play_card("Ptest", [], game_status)
