<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![tests](https://github.com/billwallis/playing-cards/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/playing-cards/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/playing-cards)](https://shields.io/badges/git-hub-last-commit)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/playing-cards/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/playing-cards/main)

</div>

---

# Playing Cards 🃏

Playing cards from the French-suited, standard 52-card pack.

## Installation ⬇️

This package is currently only available from GitHub:

```
pip install git+https://github.com/billwallis/playing-cards@v0.0.3
```

## Usage 📖

This library provides classes to represent playing cards and decks of cards.

Import the package and start using the classes. Here's an example of a simple game of _Red or Black_:

```python
import playing_cards


def ask(choices: list[str]) -> str:
    """Ask a question and return the user's choice."""
    question = f"{', '.join(choices[:-1])} or {choices[-1]}? "
    while (choice := input(question).lower()) not in choices:
        pass

    return choice


def print_cards(cards: list[playing_cards.Card]) -> None:
    """Print the faces of the cards in the list."""
    print(f"[{', '.join(card.face for card in cards)}]")


def red_or_black() -> None:
    """Play a game of Red or Black."""
    deck = playing_cards.Deck()
    cards = []

    ###  red or black
    colour_choice = ask(["red", "black"])
    cards.append(deck.take_card()), print_cards(cards)
    if cards[-1].colour != colour_choice:
        print("Wrong colour. You lose!")
        return

    ###  higher or lower (ties lose)
    hl_choice = ask(["higher", "lower"])
    cards.append(deck.take_card()), print_cards(cards)
    is_higher = cards[-1].rank > cards[-2].rank
    is_lower = cards[-1].rank < cards[-2].rank
    if not (
        (hl_choice == "higher" and is_higher)
        or (hl_choice == "lower" and is_lower)
    ):
        print("Wrong direction. You lose!")
        return

    ###  inside or outside (only inside is inclusive)
    io_choice = ask(["inside", "outside"])
    cards.append(deck.take_card()), print_cards(cards)
    rank_min, rank_max = sorted([cards[-3].rank, cards[-2].rank])
    is_inside = rank_min <= cards[-1].rank <= rank_max
    if not (
        (io_choice == "inside" and is_inside)
        or (io_choice == "outside" and not is_inside)
    ):
        print("Wrong range. You lose!")
        return

    ###  suit
    suit_choice = ask(list(playing_cards.Suit))
    cards.append(deck.take_card()), print_cards(cards)
    if cards[-1].suit != suit_choice:
        print("Wrong suit. You lose!")
        return

    print("You win!")


if __name__ == "__main__":
    red_or_black()
```

## Contributing

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and then enable [pre-commit](https://pre-commit.com/):

```bash
uv sync --all-groups
pre-commit install --install-hooks
```
