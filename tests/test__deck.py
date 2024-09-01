"""
Test the ``playing_cards`` package.
"""

import pytest

from playing_cards import Card, Deck, Rank, Suit


def test__deck__can_be_initialised():
    """
    Test that decks can be initialised.
    """
    deck = Deck()
    assert len(deck) == 52
    assert type(deck[0]) is Card
    assert repr(deck) == "Deck()"


def test__deck__taking_a_card_makes_the_deck_smaller():
    """
    Test that taking a card from the deck makes it smaller.
    """
    deck = Deck()
    card = deck.take_card()
    assert len(deck) == 51
    assert type(card) is Card
    assert card not in deck


def test__deck__card_cannot_be_taken_from_empty_deck():
    """
    Test that taking a card from an empty deck raises an error.
    """
    deck = Deck()
    [deck.take_card() for _ in range(52)]

    with pytest.raises(IndexError):
        deck.take_card()


@pytest.mark.parametrize(
    "key, card",
    [
        ("AC", Card(Rank.ACE, Suit.CLUB)),
        ("2S", Card(Rank.TWO, Suit.SPADE)),
        ("TH", Card(Rank.TEN, Suit.HEART)),
        ("KD", Card(Rank.KING, Suit.DIAMOND)),
    ],
)
def test__deck__cards_can_be_taken_by_id(key: str, card: Card):
    """
    Test that cards can be taken by ID.
    """
    deck = Deck()
    taken_card = deck.take_card(key)
    assert len(deck) == 51
    assert taken_card == card
    assert taken_card not in deck


def test__deck__card_cannot_be_taken_by_id_if_it_is_not_in_the_deck():
    """
    Test that cards cannot be taken by ID if they are not in the deck.
    """
    deck = Deck()
    deck.take_card("AS")
    with pytest.raises(KeyError):
        deck.take_card("AS")


def test__deck__can_be_reset():
    """
    Test that decks can be reset.
    """
    deck = Deck()
    [deck.take_card() for _ in range(10)]
    assert len(deck) == 42

    deck.reset()
    assert len(deck) == 52
