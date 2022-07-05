import pytest

from cards import Card, TrucoCard, Value, Suit


@pytest.mark.parametrize("value, suit", [(2, 1), (2, 2), (13, 1), (6, 3), (7, 2)])
def test_card_happy_instantiation(value, suit):
    card = Card(value, suit)

@pytest.mark.parametrize("value, suit", [(-1, 1), (1, -2), (18, 1), (6, 9), (7, 4)])
def test_card_invalid_instantiation(value, suit):
    with pytest.raises(ValueError):
        card = Card(value, suit)

@pytest.mark.parametrize("card1, card2", [(TrucoCard(Value.ONE, Suit.HEART),    TrucoCard(Value.KING, Suit.HEART)),
                                          (TrucoCard(Value.THREE, Suit.CLUBS),  TrucoCard(Value.THREE, Suit.HEART)),
                                          (TrucoCard(Value.SIX, Suit.DIAMONDS), TrucoCard(Value.FIVE, Suit.SPADES))])
def test_card_gt(card1, card2):
    assert card1 > card2

@pytest.mark.parametrize("card1, card2", [(TrucoCard(Value.ONE, Suit.HEART),    TrucoCard(Value.KING, Suit.HEART)),
                                          (TrucoCard(Value.THREE, Suit.CLUBS),  TrucoCard(Value.THREE, Suit.HEART)),
                                          (TrucoCard(Value.SIX, Suit.DIAMONDS), TrucoCard(Value.FIVE, Suit.SPADES))])
def test_card_lt(card1, card2):
    assert card2 < card1

def test_card_eq():
    assert TrucoCard(Value.THREE, Suit.CLUBS) == TrucoCard(Value.THREE, Suit.CLUBS)

def test_card_neq():
    assert TrucoCard(Value.THREE, Suit.CLUBS) != TrucoCard(Value.THREE, Suit.HEART)

def test_card_string_representation():
    assert TrucoCard(Value.THREE, Suit.CLUBS).__str__() == "3-♣"
    assert TrucoCard(Value.KING, Suit.HEART).__str__() == "K-♥"
    assert TrucoCard(Value.SEVEN, Suit.SPADES).__str__() == "7-♠"
    assert TrucoCard(Value.QUEEN, Suit.DIAMONDS).__str__() == "Q-♦"
