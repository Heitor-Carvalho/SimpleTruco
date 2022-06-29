import random

class PlayersManager:

    def __init__(self, players):
        self.players_ = players
        self.current_player_ = self.chose_random_current_player()

    def chose_random_current_player(self):
        return random.choice(self.players_)

    def get_players(self):
        return self.players_

    def get_current_player(self):
        return self.current_player_

    def get_next_player(self):
        index = self.players_.index(self.current_player_)
        return self.players_[(index + 1) % len(self.players_)]

    def move_next_player(self):
        index = self.players_.index(self.current_player_)
        self.current_player_ = self.players_[(index + 1) % len(self.players_)]

class Player:

    def __init__(self, strategy, name):
        self.strategy_ = strategy
        self.cards_ = []
        self.name_ = name

    def name(self):
        return self.name_

    def handle_cards(self, cards):
        self.cards_ = cards

    def make_chalange(self, game_status):
        return self.strategy_.make_chalange(self.name_, self.cards_, game_status)

    def handle_chalange(self, game_status):
        return self.strategy_.handle_chalange(self.name_, self.cards_, game_status)

    def play_card(self, game_status):
        return self.strategy_.play_card(self.cards_, game_status)

    def clean_cards(self):
        self.cards_ = []

class UserStretagy:

    def show_hand(self, cards):
        print("Player Hands:")
        for index, card in enumerate(cards):
            print(f"Card {index+1}: {card}")

    def make_chalange(self, name, cards, game_status):
        print(f"Current user {name}")

        self.show_hand(cards)
        print("0 - No Truco [default]")
        print("1 - Truco")
        truco = 0
        try:
            truco = int(input("Truco?: "))
        except Exception:
            truco = 0

        return truco == 1

    def handle_chalange(self, name, cards, game_status):
        try:
            print(f"Current user {name}")
        except Exception as e:
            print(f"Error: str(e)")

        self.show_hand(cards)
        print("0 - Accept")
        print("1 - Denied [default]")
        accept = 0
        try:
            accept = int(input("Accept?: "))
        except Exception:
            accept = 1

        return accept == 0

    def play_card(self, cards, game_status):
        self.show_hand(cards)
        card_nb = -1
        while (card_nb < 0 or card_nb >= len(cards)):
            try:
                card_nb = int(input("Choose a card: "))-1
            except Exception:
                pass

        card = cards.pop(card_nb)
        return card

class DummyStretagy:

    def make_chalange(self, cards, game_status):
        return False

    def handle_chalange(self, cards, game_status):
        return True

    def play_card(self, cards, game_status):
        if len(cards) != 0:
            return cards.pop()
        else:
            print("No cards avaliable")



#if __name__ == "__main__":
#    dummy_strategy = DummyStretagy()
#    p1 = Player(dummy_strategy)
#    from game_status import GameStatus
#    game_status = GameStatus()
#    print(p1.make_chalange(game_status))
#    print(p1.handle_chalange(game_status))
#
#    from cards import TrucoCard
#    cards = [TrucoCard(2, 1),
#             TrucoCard(1, 2),
#             TrucoCard(3, 2)]
#    print(p1.handle_cards(cards))
#    print(p1.play_card(game_status))

