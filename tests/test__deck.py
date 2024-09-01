"""
Test the ``playing_cards`` package.
"""

import pytest

from playing_cards import Card, Deck, Rank, Suit


###
# Deck tests
###
def test__deck():
    """
    Test the construction of the ``Deck`` class.
    """
    deck_1 = Deck()
    deck_2 = Deck(num_decks=2)

    assert deck_1._num_decks == 1
    assert deck_2._num_decks == 2
    assert str(deck_1) == "Deck consisting of 52 cards"
    assert str(deck_2) == "Deck consisting of 104 cards"
    assert repr(deck_1) == f"Deck(num_decks={deck_1._num_decks})"
    assert repr(deck_2) == f"Deck(num_decks={deck_2._num_decks})"
    assert len(deck_1) == 52
    assert len(deck_2) == 104
    assert type(deck_1[0]) is Card
    assert type(deck_2[0]) is Card


def test__deck__take_card():
    """
    Test the ``Deck.take_card()`` method.
    """
    deck_ = Deck()
    assert len(deck_) == 52
    card = deck_.take_card()
    assert len(deck_) == 51
    assert type(card) is Card
    assert card not in deck_


@pytest.mark.parametrize(
    "key, card",
    [
        ("AC", Card(Rank.ACE, Suit.CLUB)),
        ("2S", Card(Rank.TWO, Suit.SPADE)),
        ("TH", Card(Rank.TEN, Suit.HEART)),
        ("KD", Card(Rank.KING, Suit.DIAMOND)),
    ],
)
def test__deck__take_card_by_key(key: str, card: Card):
    """
    Test the ``Deck._take_card_by_key()`` method.
    """
    deck_ = Deck()
    taken_card = deck_._take_card_by_key(key)
    assert len(deck_) == 51
    assert taken_card == card
    assert taken_card not in deck_


@pytest.mark.parametrize(
    "key, card",
    [
        ("AC", Card(Rank.ACE, Suit.CLUB)),
        ("2S", Card(Rank.TWO, Suit.SPADE)),
        ("TH", Card(Rank.TEN, Suit.HEART)),
        ("KD", Card(Rank.KING, Suit.DIAMOND)),
    ],
)
def test__deck__take_card_by_key__multiple_decks(key: str, card: Card):
    """
    Test the ``Deck._take_card_by_key()`` method on multiple decks.
    """
    deck_ = Deck(num_decks=3)
    taken_card_1 = deck_._take_card_by_key(key)
    taken_card_2 = deck_._take_card_by_key(key)
    taken_card_3 = deck_._take_card_by_key(key)
    assert len(deck_) == (52 * 3) - 3
    assert taken_card_1 == taken_card_2 == taken_card_3 == card
    assert taken_card_1 not in deck_
