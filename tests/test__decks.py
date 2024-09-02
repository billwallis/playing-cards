"""
Test the ``playing_cards`` package.
"""

import pytest

from playing_cards import Card, Decks, Rank, Suit


def test__decks__can_be_initialised():
    """
    Test that decks can be initialised.
    """
    deck_1, deck_2, deck_3 = Decks(1), Decks(2), Decks(3)
    assert len(deck_1) == 52
    assert len(deck_2) == 104
    assert len(deck_3) == 156


def test__decks__taking_a_card_makes_the_deck_smaller():
    """
    Test that taking a card from the deck makes it smaller.
    """
    deck = Decks(2)
    card = deck.take_card()
    assert len(deck) == 103
    assert type(card) is Card
    assert card in deck


def test__decks__card_cannot_be_taken_from_empty_deck():
    """
    Test that taking a card from an empty deck raises an error.
    """
    deck = Decks(2)
    [deck.take_card() for _ in range(104)]

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
def test__decks__cards_can_be_taken_by_id(key: str, card: Card):
    """
    Test the ``Deck._take_card_by_key()`` method.
    """
    deck = Decks(2)
    taken_card = deck.take_card(key)
    assert len(deck) == 103
    assert taken_card == card
    assert taken_card in deck


def test__decks__multiple_cards_can_be_taken_by_id():
    """
    Test the ``Deck._take_card_by_key()`` method.
    """
    key = "AS"
    card = Card.from_id(key)
    deck = Decks(2)

    taken_card_1 = deck.take_card(key)
    assert len(deck) == 103
    assert taken_card_1 == card
    assert taken_card_1 in deck

    taken_card_2 = deck.take_card(key)
    assert len(deck) == 102
    assert taken_card_2 == card
    assert taken_card_2 not in deck


def test__decks__card_cannot_be_taken_by_id_if_it_is_not_in_the_deck():
    """
    Test the ``Deck._take_card_by_key()`` method.
    """
    deck = Decks(2)
    deck.take_card("AS")
    deck.take_card("AS")
    with pytest.raises(KeyError):
        deck.take_card("AS")


def test__decks__can_be_reset():
    """
    Test that decks can be reset.
    """
    deck = Decks(2)
    [deck.take_card() for _ in range(10)]
    assert len(deck) == 94

    deck.reset()
    assert len(deck) == 104
