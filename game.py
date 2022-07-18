from enum import Enum

from game_status import GameStatus, TrucoChallengeStatus
from cards import Value


from abc import ABC, abstractmethod

class TrucoGame:


    class TrucoGameEvents(Enum):
        STATE_GAME_INIT             = 0
        STATE_ROUNDS_PREPARE        = 1
        STATE_ROUND_START           = 2
        STATE_ROUND_TRUCO_CHALLENGE = 3
        STATE_ROUND_TRUCO_ACCEPT    = 4
        STATE_ROUNDS_PLAY_CARD      = 5
        STATE_ROUND_RESOLVE         = 6
        STATE_ROUNDS_END            = 7
        STATE_GAME_END              = 8

    class StateContext:

        def __init__(self, deck_builder, player_manager):
            self.deck_builder = deck_builder
            self.player_manager = player_manager
            self.deck = None
            self.game_status = None

    class State:

        listeners = []
        context = None

        @classmethod
        def set_context(cls, context_arg):
            cls.context = context_arg

        @classmethod
        def check_game_end(cls, context):
                return context.game_status.get_team_a_score() >= 12 or \
                       context.game_status.get_team_b_score() >= 12

        @classmethod
        def check_round_end(cls, context):
            truco_status = context.game_status.get_round_status().get_truco_status()
            return context.game_status.get_round_status().get_round_turn() == 3 or \
                   context.game_status.get_round_status().get_team_a_round_score() == 2 or \
                   context.game_status.get_round_status().get_team_b_round_score() == 2 or \
                   (truco_status.challenge_accepted == False and truco_status.challenge_status == True)

        @classmethod
        def register_event_listener(cls, listener):
            cls.listeners.append(listener)

        @classmethod
        def emit_event(cls, event, context):
            data = (context.player_manager.get_current_player().name(), context.game_status)
            for listener in cls.listeners:
                listener.handle_event(event, data)

    class StateGameInit(State):

        def execute(self):
            context = TrucoGame.State.context
            context.game_status = GameStatus()
            context.game_status.add_to_team_a(context.player_manager.get_current_player().name())
            context.game_status.add_to_team_b(context.player_manager.get_next_player().name())

        def external_input(self):
            context = TrucoGame.State.context
            return TrucoGame.State.check_game_end(context)

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_GAME_INIT, context)
            context.player_manager.get_current_player().ask_press()
            context.player_manager.get_next_player().ask_press()

    class StateRoundsPreprare:

        def execute(self):
            context = TrucoGame.State.context
            context.deck = context.deck_builder.build_truco_deck()
            context.deck.shuffle()
            context.game_status.reset_round_status()

            for player in context.player_manager.get_players():
                player.clean_cards()
                player.handle_cards(context.deck.get_n_cards(3))

        def external_input(self):
            return True

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUNDS_PREPARE, context)

        def _check_round_end(self, context):
            truco_status, _ = context.game_status_.get_round_status().get_truco_status()
            return check_round_end(context)

    class StateGameEnd:

        def execute(self):
            pass

        def external_input(self):
            return True

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_GAME_END, context)
            context.player_manager.get_current_player().ask_press()
            context.player_manager.get_next_player().ask_press()

    class StateRoundStart:

        def execute(self):
            context = TrucoGame.State.context
            central_card = context.deck.get_n_cards(1)[0]
            context.game_status.get_round_status().set_central_card(central_card)

        def external_input(self):
            return True

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUND_START, context)
            context.player_manager.get_current_player().ask_press()

    class StateRoundTrucoChallenge:

        def execute(self):
            context = TrucoGame.State.context
            truco_status = TrucoChallengeStatus()
            truco_status.challenge_status = context.player_manager.get_current_player().make_challenge(context.game_status) and \
                                            context.game_status.get_round_status().get_round_points() < 12
            truco_status.challenger_player = context.player_manager.get_current_player().name()
            truco_status.challenged_player = context.player_manager.get_next_player().name()

            context.game_status.get_round_status().set_truco_status(truco_status)

        def external_input(self):
            context = TrucoGame.State.context
            return context.game_status.get_round_status().get_truco_status().challenge_status

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUND_TRUCO_CHALLENGE, context)

    class StateRoundTrucoAccept(State):

        def execute(self):
            #self.player_manager.get_current_player().ask_press()
            challenged_accepted = self._accept_challenge()
            return challenged_accepted

        def external_input(self):
            context = TrucoGame.State.context
            return context.game_status.get_round_status().get_truco_status().challenge_accepted

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUND_TRUCO_ACCEPT, context)

        def _accept_challenge(self):
            context = TrucoGame.State.context
            truco_status = context.game_status.get_round_status().get_truco_status()
            truco_status.challenge_accepted = context.player_manager.get_next_player().handle_challenge(context.game_status)
            if truco_status.challenge_accepted:
                context.game_status.get_round_status().increase_round_points()

    class StateRoundPlayCard:

        def execute(self):
            context = TrucoGame.State.context

            card_current_player = context.player_manager.get_current_player().play_card(context.game_status)
            context.game_status.add_played_card(context.player_manager.get_current_player().name(), card_current_player)
            context.player_manager.move_next_player()

            card_current_player = context.player_manager.get_current_player().play_card(context.game_status)
            context.game_status.add_played_card(context.player_manager.get_current_player().name(), card_current_player)
            context.player_manager.move_next_player()

        def external_input(self):
            return True

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUNDS_PLAY_CARD, context)

    class StateRoundResolve:

        def execute(self):
            context = TrucoGame.State.context
            self._resolve_round(context)

        def external_input(self):
            context = TrucoGame.State.context
            return TrucoGame.State.check_round_end(context)

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUND_RESOLVE, context)

        def _resolve_round(self, context):
            truco_status = context.game_status.get_round_status().get_truco_status()
            if truco_status.challenge_status == True and \
               truco_status.challenge_accepted == False:
                context.game_status.increment_player_round_team_score(truco_status.challenger_player)
                context.game_status.get_round_status().set_round_winner(truco_status.challenger_player)
            else:
                if self._compare_cards(context.game_status.get_round_status().get_central_card(),
                                       context.game_status.get_round_status().get_team_a_played_cards()[-1],
                                       context.game_status.get_round_status().get_team_b_played_cards()[-1]):
                    context.game_status.get_round_status().increment_team_a_round_score()
                    context.game_status.get_round_status().set_round_winner(context.game_status.get_team_a_player())
                else:
                    context.game_status.get_round_status().increment_team_b_round_score()
                    context.game_status.get_round_status().set_round_winner(context.game_status.get_team_b_player())

                context.game_status.get_round_status().increase_round_turn()

        def _compare_cards(self, central_card, card1, card2):
            if card1.value_.value == (central_card.value_.value + 1 % Value.KING) and \
                    card2.value_.value == (central_card.value_.value + 1 % Value.KING):
                return card1.suit_ < card2.suit_
            if card1.value_.value == (central_card.value_.value + 1 % Value.KING):
                return True
            if card2.value_.value == (central_card.value_.value + 1 % Value.KING):
                return False

            return card1 > card2


    class StateRoundsEnd:

        def execute(self):
            context = TrucoGame.State.context
            if context.game_status.get_round_status().get_team_a_round_score() > \
               context.game_status.get_round_status().get_team_b_round_score():
                context.game_status.increment_team_a_game_score()
            else:
                context.game_status.increment_team_b_game_score()

            context.player_manager.get_current_player().ask_press()
            context.player_manager.move_next_player()

        def external_input(self):
            context = TrucoGame.State.context
            return TrucoGame.State.check_game_end(context)

        def pos_execute(self):
            context = TrucoGame.State.context
            TrucoGame.State.emit_event(TrucoGame.TrucoGameEvents.STATE_ROUNDS_END, context)
            context.player_manager.get_current_player().ask_press()
            context.player_manager.get_next_player().ask_press()

    def __init__(self, player_manager, deck_builder, handlers=[]):
        self.handlers_ = handlers

        self._context = TrucoGame.StateContext(deck_builder, player_manager)

        TrucoGame.State.set_context(self._context)

        self.state_game_init             = TrucoGame.StateGameInit()
        self.state_rounds_prepare        = TrucoGame.StateRoundsPreprare()
        self.state_round_start           = TrucoGame.StateRoundStart()
        self.state_round_truco_challange = TrucoGame.StateRoundTrucoChallenge()
        self.state_round_truco_accept    = TrucoGame.StateRoundTrucoAccept()
        self.state_round_play_cards      = TrucoGame.StateRoundPlayCard()
        self.state_round_resolve         = TrucoGame.StateRoundResolve()
        self.state_rounds_end            = TrucoGame.StateRoundsEnd()
        self.state_game_end              = TrucoGame.StateGameEnd()

                         # (current state,                     input)  -->  next_state
        self.transition = {(self.state_game_init,              False):      self.state_rounds_prepare,
                           (self.state_game_init,              True):       self.state_game_end,

                           (self.state_rounds_prepare,         True):       self.state_round_start,

                           (self.state_round_start,            True):       self.state_round_truco_challange,

                           (self.state_round_truco_challange,  True):       self.state_round_truco_accept,
                           (self.state_round_truco_challange,  False):      self.state_round_play_cards,

                           (self.state_round_truco_accept,     True):       self.state_round_truco_challange,
                           (self.state_round_truco_accept,     False):      self.state_round_resolve,

                           (self.state_round_play_cards,       True):       self.state_round_resolve,

                           (self.state_round_resolve,          True):       self.state_rounds_end,
                           (self.state_round_resolve,          False):      self.state_round_start,

                           (self.state_rounds_end,             False):      self.state_rounds_prepare,
                           (self.state_rounds_end,             True):       self.state_game_end}

    def start(self):
        pass

    def finish(self):
        pass

    def get_next_state(self, state, external_input):
        return self.transition[(state, external_input)]

    def run(self):
        self.state = self.state_game_init
        while self.state != self.state_game_end:
            print(self.state)
            self.state.execute()
            self.state.pos_execute()
            external_input = self.state.external_input()
            self.state = self.get_next_state(self.state, external_input)

    def register_event_listener(self, handler):
        TrucoGame.State.register_event_listener(handler)

