from cards import DeckBuilder
from view import ConsoleView, ServerView
from game import TrucoGame
from player import Player, PlayersManager
from events_handlers import ConsoleViewDisplay
from game_strategies import DummyStretagy, UserStretagy

# TODO Implement other strategy
# TODO Add nice logging
# TODO Review error handling
# TODO Write tests
# TODO Turn game in a state machine

if __name__ == "__main__":
    deck_builder = DeckBuilder()

    #view = ServerView("127.0.0.1", 4022)
    view = ConsoleView()
    view.start()
    console_view_control = ConsoleViewDisplay(view)

    #l1_user_strategy = UserStretagy(view)
    l1_user_strategy = DummyStretagy()
    l2_user_strategy = DummyStretagy()
    #l2_user_strategy = UserStretagy(view)

    l1_player = Player(l1_user_strategy, "Player 1")
    l2_player = Player(l2_user_strategy, "Player 2")

    players = [l1_player, l2_player]
    player_manager = PlayersManager(players)

    truco_game = TrucoGame(player_manager, deck_builder)
    truco_game.register_event_listener(console_view_control)

    truco_game.start()
    truco_game.run()
    truco_game.finish()

    view.finish()
