import pytest
from mock import Mock

from view import View
from game import TrucoGame
from game_status import GameStatus
from events_handlers import ConsoleViewDisplay



@pytest.fixture
def game_status():
    return GameStatus()

@pytest.fixture
def mock_view():
    return Mock(View)

@pytest.fixture
def console_display(mock_view):
    return ConsoleViewDisplay(mock_view)


def test_event_handler_game_init(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_GAME_INIT, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_game_status.assert_called_once()

def test_event_handler_rounds_prepare(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUNDS_PREPARE, ("PTest", game_status))
    console_display.handle_event(event, data)

def test_event_handler_round_start_no_players(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUND_START, ("PTest", game_status))
    with pytest.raises(IndexError):
        console_display.handle_event(event, data)

def test_event_handler_round_truco_challenge(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUND_TRUCO_CHALLENGE, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_truco_chalange_message.assert_called_once()

def test_event_handler_round_truco_accept(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUND_TRUCO_ACCEPT, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_truco_accept_message.assert_called_once()

def test_event_handler_round_truco_resolve_no_players(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUND_RESOLVE, ("PTest", game_status))
    with pytest.raises(IndexError):
        console_display.handle_event(event, data)

def test_event_handler_rounds_end(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUNDS_END, ("PTest", game_status))
    with pytest.raises(IndexError):
        console_display.handle_event(event, data)

def test_event_handler_game_end(console_display, game_status, mock_view):
    (event, data) = (TrucoGame.TrucoGameEvents.STATE_GAME_END, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_end_game.assert_called_once()

def test_event_handler_rounds_resolve(console_display, game_status, mock_view):
    game_status.add_to_team_a("P1Test")
    game_status.add_to_team_b("P2Test")

    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUND_RESOLVE, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_round_status.assert_called_once()

def test_event_handler_round_start(console_display, game_status, mock_view):
    game_status.add_to_team_a("P1Test")
    game_status.add_to_team_b("P2Test")

    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUND_START, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_round_status.assert_called_once()

def test_event_handler_round_end(console_display, game_status, mock_view):
    game_status.add_to_team_a("P1Test")
    game_status.add_to_team_b("P2Test")

    (event, data) = (TrucoGame.TrucoGameEvents.STATE_ROUNDS_END, ("PTest", game_status))
    console_display.handle_event(event, data)
    mock_view.show_round_end.assert_called_once()
    mock_view.show_game_status.assert_called_once()

