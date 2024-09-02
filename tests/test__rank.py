"""
Test the ``playing_cards.Rank`` class.
"""

import pytest

from playing_cards import Rank


@pytest.mark.parametrize(
    "rank_value",
    range(1, 14),
)
def test__rank__can_be_initialised(rank_value: int):
    """
    Test that ranks can be initialised.
    """
    rank = Rank(rank_value)
    assert rank.value == rank_value
    assert str(rank) == str(rank_value)
    assert repr(rank) == f"<Rank.{rank.name}: {rank.value}>"


@pytest.mark.parametrize(
    "rank_1, rank_2, expected",
    [
        (Rank.ACE, Rank.ACE, False),
        (Rank.ACE, Rank.TWO, True),
        (Rank.ACE, Rank.TEN, True),
        (Rank.ACE, Rank.KING, True),
        (Rank.TWO, Rank.ACE, False),
        (Rank.TWO, Rank.TWO, False),
        (Rank.TWO, Rank.TEN, True),
        (Rank.TWO, Rank.KING, True),
        (Rank.TEN, Rank.ACE, False),
        (Rank.TEN, Rank.TWO, False),
        (Rank.TEN, Rank.TEN, False),
        (Rank.TEN, Rank.KING, True),
        (Rank.KING, Rank.ACE, False),
        (Rank.KING, Rank.TWO, False),
        (Rank.KING, Rank.TEN, False),
        (Rank.KING, Rank.KING, False),
    ],
)
def test__rank__can_be_compared_as_a_total_order(
    rank_1: Rank,
    rank_2: Rank,
    expected: bool,
):
    """
    Test that ranks can be compared as a total order.
    """
    assert (rank_1 < rank_2) is expected
    assert (rank_1 >= rank_2) is not expected
    assert (rank_1 == rank_1) is True  # noqa: PLR0124
    assert (rank_1 != rank_1) is False  # noqa: PLR0124


@pytest.mark.parametrize(
    "id_, rank",
    [
        ("A", Rank.ACE),
        ("2", Rank.TWO),
        ("6", Rank.SIX),
        ("T", Rank.TEN),
        ("J", Rank.JACK),
        ("Q", Rank.QUEEN),
        ("K", Rank.KING),
    ],
)
def test__rank__can_be_initialised_from_an_id(id_: str, rank: Rank):
    """
    Test that ranks can be initialised from an ID.
    """
    assert Rank.from_id(id_) == rank


def test__rank__cannot_be_initialised_from_an_invalid_id():
    """
    Test that ranks cannot be initialised from an invalid ID.
    """
    with pytest.raises(KeyError):
        Rank.from_id("X")
