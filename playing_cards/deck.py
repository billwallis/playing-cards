"""
Define the cards and decks.

A deck in the traditional sense is a collection of 52 playing cards from
the French-suited, standard 52-card pack.

A ``Deck`` in this module is ``n`` sets of decks (making it a slight
misnomer), where a ``Card`` class represents each playing card.

There are currently no Joker cards in the ``Card`` class.
"""

from __future__ import annotations

import dataclasses
import enum
import functools
import itertools
import pathlib
import random
import tomllib
from typing import Any, Literal

Colour = Literal["black", "red"]

SUITS: dict[str, dict[str, str]] = tomllib.loads(
    pathlib.Path("playing_cards/suits.toml").read_text(encoding="utf-8")
)
RANKS: dict[str, dict[str, str]] = tomllib.loads(
    pathlib.Path("playing_cards/ranks.toml").read_text(encoding="utf-8")
)


class Suit(enum.StrEnum):
    """
    A suit for a playing card.
    """

    CLUB = "club"
    SPADE = "spade"
    HEART = "heart"
    DIAMOND = "diamond"

    @functools.total_ordering
    def __lt__(self, other: Suit) -> bool:
        order = {
            Suit.CLUB: 0,
            Suit.DIAMOND: 1,
            Suit.HEART: 2,
            Suit.SPADE: 3,
        }
        return order[self] < order[other]

    def _get(self, _key: Any, /) -> Any:
        """
        Return the value of the key.
        """
        return SUITS[self.value][_key]  # type: ignore

    @classmethod
    def from_id(cls, _id: str, /) -> Suit:
        """
        Return a ``Rank`` from its corresponding character.

        :raises KeyError: If the key does not correspond to a valid suit.
        """
        for suit, properties in SUITS.items():
            if properties["id"] == _id:
                return cls(suit)

        raise KeyError(f"The key '{_id}' is not a valid suit")

    @property
    def id(self) -> str:
        """
        The single character corresponding to the suit.
        """
        return self._get("id")

    @property
    def image(self) -> str:
        """
        The image corresponding to the suit.
        """
        return self._get("image")

    @property
    def colour(self) -> Colour:
        """
        The colour corresponding to the suit.
        """
        return self._get("colour")


class Rank(enum.IntEnum):
    """
    A rank for a playing card.

    Note that Ace is low in this implementation.
    """

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13

    @functools.total_ordering
    def __lt__(self, other: Rank) -> bool:
        return self.value < other.value

    def _get(self, _key: Any, /) -> Any:
        """
        Return the value of the key.
        """
        return RANKS[str(self.value)][_key]  # type: ignore

    @classmethod
    def from_id(cls, _id: str, /) -> Rank:
        """
        Return a ``Rank`` from its corresponding character.
        """
        for rank, properties in RANKS.items():
            if properties["id"] == _id:
                return cls(int(rank))

        raise KeyError(f"The key '{_id}' is not a valid rank")

    @property
    def id(self) -> str:
        """
        The single character corresponding to the rank.
        """
        return self._get("id")


@dataclasses.dataclass
class Card:
    """
    A playing card from the French-suited, standard 52-card pack.
    """

    rank: Rank
    suit: Suit

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank.id + self.suit.id

    @classmethod
    def from_id(cls, _key: str, /) -> Card:
        """
        Return a ``Card`` corresponding to the string.
        """
        if len(_key) != 2:  # noqa: PLR2004
            raise KeyError(f"The key, {_key}, should be 2 characters")
        return cls(Rank.from_id(_key[0]), Suit.from_id(_key[1]))

    @property
    def face(self) -> str:
        """
        The face of the card.

        This shows the rank and then the image of the suit.
        """
        return self.rank.id + self.suit.image

    @property
    def value(self) -> int:
        """
        The value of the card.
        """
        return self.rank.value

    @property
    def colour(self) -> Colour:
        """
        The colour of the card.
        """
        return self.suit.colour


class Deck:
    """
    A class to represent a multiple sets of 52-card French-suited deck that
    may or may not have all cards in them.

    This name is a misnomer, since it can actually be many sets of decks
    (where "deck" means a set of 52 cards).
    """

    _num_decks: int
    cards: list[Card]

    def __init__(self, num_decks: int = 1):
        """
        Return a ``Deck`` with ``num_decks`` decks in it.

        :param num_decks: The number of 52-card decks to include.
        """
        self._num_decks = num_decks
        self.cards = []
        self.reset()

    def __str__(self):
        s = (
            "" if len(self) == 1 else "s"
        )  # sourcery skip: avoid-single-character-names-variables
        return f"Deck consisting of {len(self)} card{s}"

    def __repr__(self):
        return f"Deck(num_decks={self._num_decks})"

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def reset(self) -> None:
        """
        Reset the deck to have all cards in it, then shuffle it.
        """
        self.cards = [
            Card(rank, suit)
            for _, rank, suit in itertools.product(
                range(self._num_decks), Rank, Suit
            )
        ]

        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffle the deck.
        """
        random.shuffle(self.cards)

    def take_card(self, _key: str = None) -> Card:
        """
        Return the top card from the deck.

        :param _key: The key of the card to take.

        :return: A list of the taken cards.
        """
        return self._take_card_by_key(_key) if _key else self.cards.pop()

    def _take_card_by_key(self, key: str) -> Card:
        """
        Pop the card from the deck whose key corresponds to ``key``.

        This is just for debugging and testing.

        :param key: The key of the card to take.

        :raises IndexError: If the card has already been removed from the deck.

        :return: A list of cards corresponding to the key.
        """
        for i, card in enumerate(self.cards):
            if str(card) == key:
                return self.cards.pop(i)
