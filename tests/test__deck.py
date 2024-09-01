"""
Test the ``playing_cards`` package.
"""

import itertools

import pytest

from playing_cards import Card, Colour, Deck, Rank, Suit


###
# Card tests
###
def test__card():
    """
    Test the construction of the ``Card`` class.
    """
    for rank, suit in itertools.product(Rank, Suit):
        card = Card(rank, suit)
        assert card.rank == rank
        assert card.suit == suit
        assert str(card) == rank.id + suit.id
        assert repr(card) == f"Card({rank=}, {suit=})"


@pytest.mark.parametrize(
    "card, other, result",
    [
        (Card.from_str("2S"), Card.from_str("TC"), {12}),
        (Card.from_str("TC"), Card.from_str("TC"), {20}),
        (Card.from_str("2S"), 10, {12}),
        (Card.from_str("TC"), 10, {20}),
    ],
)
def test__card__add(card: Card, other: int | Card, result: set[int]):
    """
    Test the ``Card.__add__()`` method.
    """
    assert card + other == result
    assert other + card == result


def test__card__add__raises():
    """
    Test that ``Card.__add__()`` raises a ``TypeError``.
    """
    with pytest.raises(TypeError):
        Card.from_str("2S") + "2"  # type: ignore


def test__card__from_str():
    """
    Test the ``Card.from_str()`` method.
    """
    for rank, suit in itertools.product(Rank, Suit):
        card = Card.from_str(rank.id + suit.id)
        assert card.rank == rank
        assert card.suit == suit


@pytest.mark.parametrize(
    "text, error",
    [
        ("A", KeyError),
        ("ABC", KeyError),
        ("S1", KeyError),
        ("B2", KeyError),
    ],
)
def test__card__from_str__raises(text: str, error: type[Exception]):
    """
    Test that the ``Card.from_str()`` method throws exceptions.
    """
    with pytest.raises(error):
        Card.from_str(text)


@pytest.mark.parametrize(
    "rank, values",
    [
        (Rank.ACE, {1, 11}),
        (Rank.TWO, {2}),
        (Rank.THREE, {3}),
        (Rank.FOUR, {4}),
        (Rank.FIVE, {5}),
        (Rank.SIX, {6}),
        (Rank.SEVEN, {7}),
        (Rank.EIGHT, {8}),
        (Rank.NINE, {9}),
        (Rank.TEN, {10}),
        (Rank.JACK, {10}),
        (Rank.QUEEN, {10}),
        (Rank.KING, {10}),
    ],
)
def test__card__values(rank: Rank, values: set[int]):
    for suit in Suit:
        card = Card(rank, suit)  # type: ignore
        assert card.values == values


@pytest.mark.parametrize(
    "card, face",
    [
        (Card(Rank.ACE, Suit.CLUB), "A♣"),
        (Card(Rank.TWO, Suit.SPADE), "2♠"),
        (Card(Rank.TEN, Suit.HEART), "T♥"),
        (Card(Rank.KING, Suit.DIAMOND), "K♦"),
    ],
)
def test__card__face(card: Card, face: str):
    assert card.face == face


@pytest.mark.parametrize(
    "card, colour",
    [
        (Card(Rank.ACE, Suit.CLUB), "black"),
        (Card(Rank.TWO, Suit.SPADE), "black"),
        (Card(Rank.TEN, Suit.HEART), "red"),
        (Card(Rank.KING, Suit.DIAMOND), "red"),
    ],
)
def test__colour(card: Card, colour: Colour):
    assert card.colour == colour


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
