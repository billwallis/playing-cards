"""
Test the ``playing_cards.Suit`` class.
"""

import pytest

from playing_cards import Suit


@pytest.mark.parametrize(
    "suit_name",
    ["club", "spade", "heart", "diamond"],
)
def test__suit__can_be_initialised(suit_name: str):
    """
    Test that suits can be initialised.
    """
    suit = Suit(suit_name)
    assert suit.name == suit_name.upper()
    assert suit.value == suit_name.lower()
    assert suit.id == suit_name[0].upper()
    assert str(suit) == suit_name
    assert repr(suit) == f"<Suit.{suit.name}: '{suit.value}'>"


@pytest.mark.parametrize(
    "suit_1, suit_2, expected",
    [
        (Suit.CLUB, Suit.CLUB, False),
        (Suit.CLUB, Suit.SPADE, True),
        (Suit.CLUB, Suit.HEART, True),
        (Suit.CLUB, Suit.DIAMOND, True),
        (Suit.SPADE, Suit.CLUB, False),
        (Suit.HEART, Suit.CLUB, False),
        (Suit.DIAMOND, Suit.CLUB, False),
    ],
)
def test__suit__can_be_compared_as_a_total_order(
    suit_1: Suit,
    suit_2: Suit,
    expected: bool,
):
    """
    Test that suits can be compared as a total order.
    """
    assert (suit_1 < suit_2) is expected
    assert (suit_1 >= suit_2) is not expected
    assert (suit_1 == suit_1) is True  # noqa: PLR0124
    assert (suit_1 != suit_1) is False  # noqa: PLR0124


@pytest.mark.parametrize(
    "id_, suit",
    [
        ("C", Suit.CLUB),
        ("S", Suit.SPADE),
        ("H", Suit.HEART),
        ("D", Suit.DIAMOND),
    ],
)
def test__suit__can_be_initialised_from_an_id(id_: str, suit: Suit):
    """
    Test that suits can be initialised from an ID.
    """
    assert Suit.from_id(id_) == suit


def test__suit__cannot_be_initialised_from_an_invalid_id():
    """
    Test that suits cannot be initialised from an invalid ID.
    """
    with pytest.raises(KeyError):
        Suit.from_id("X")
