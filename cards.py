import random
from enum import IntEnum

class Suit(IntEnum):
    DIAMONDS = 0
    SPADES   = 1
    HEART    = 2
    CLUBS    = 3

    def __str__(self):
        suits_map = '♦♠♥♣'
        return suits_map[self.value]

class Value(IntEnum):
    ONE   = 1
    TWO   = 2
    THREE = 3
    FOUR  = 4
    FIVE  = 5
    SIX   = 6
    SEVEN = 7
    EIGHT = 8
    NINE  = 9
    TEN   = 10
    QUEEN = 11
    JACK  = 12
    KING  = 13

    def __str__(self):
        if self.value == Value.QUEEN:
            return "Q"
        elif self.value == Value.JACK:
            return "J"
        elif self.value == Value.KING:
            return "K"
        else:
            return str(self.value)

class Card:

    def __init__(self, value, suit):
        self.value_ = Value(value)
        self.suit_  = Suit(suit)

    def __str__(self):
        return f"{self.value_}-{self.suit_}"


class TrucoCard(Card):

    one_two_three = {Value.ONE, Value.TWO, Value.THREE}

    def __eq__(self, other):
        return self.value_ == other.value_ and \
               self.suit_ == other.suit_

    def __gt__(self, other):
        if self.value_ == other.value_:
            return self.suit_ > other.suit_
        else:
            if self.value_ in TrucoCard.one_two_three and \
               other.value_ in TrucoCard.one_two_three:
                return self.value_ > other.value_
            elif self.value_ not in TrucoCard.one_two_three and \
                 other.value_ not in TrucoCard.one_two_three:
                return self.value_ > other.value_
            else:
                if self.value_ in TrucoCard.one_two_three:
                    return True
                else:
                    return False

    def __lt__(self, other):
        return not (self > other)


class Deck:

    def __init__(self, cards):
        self.cards = cards

    def show_deck(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def get_n_cards(self, n=1):
        draw_cards = []
        for _ in range(0, n):
            if len(self.cards) != 0:
                draw_cards.append(self.cards.pop())
        return draw_cards


class DeckBuilder:

    def rebuild(self):
        return self.build_truco_deck()

    @staticmethod
    def build_truco_deck():
        cards = []
        for val in list(Value)[0:7] + list(Value)[10:]:
            for suit in list(Suit):
                cards.append(TrucoCard(val, suit))
        return Deck(cards)
