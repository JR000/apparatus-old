from sqlite3 import Time
from typing import Optional
from uuid import UUID


class Book:
    id: UUID
    title: str
    author: str
    cards: Optional[list["Card"]]
    sections: Optional[list["Section"]]
    tokens: Optional["Token"]

class Card:
    id: UUID
    type: str
    paragraphs: Optional[list["Paragraph"]]
    ordinal: Optional[int]
    parent: Optional["Section"]
    carried_tokens: Optional[list["Token"]]
    requirements: Optional[list["TokenRequirement"]]

class Token:
    id: UUID
    title: str
    requirements: Optional[list["TokenRequirement"]]
    cards_carry: Optional[list["Card"]]

class Paragraph:
    id: UUID
    type: str
    value: any
    ordinal: Optional[int]

    card: Optional["Card"]
    parent: Optional["Paragraph"]
    subparagrpahs: Optional[list["Paragraph"]]

class Section:
    id: UUID
    type: str
    ordinal: int

    subsections: Optional[list["Section"]]
    parent: Optional["Section"]
    cards: Optional[list["Card"]]

class TokenRequirement:
    token: Optional["Token"]
    card: Optional["Card"]
    data: Optional[any] # optional, потому что можно использовать и без: например, чтобы подчеркнуть наличие зависимости

class TokenSchedule:
    token: Optional["Token"]
    system: str
    timastamp: any # TODO: исправить типизацию
    puzzle: Optional["CardPuzzle"]
    data: any # TODO: исправить типизацию

class CardSchedule:
    card: Optional["Card"]
    system: str
    timastamp: any # TODO: исправить типизацию
    puzzle: Optional["CardPuzzle"]
    data: any # TODO: исправить типизацию

class CardPuzzle:
    card: Optional["Card"]
    quality: float
    type: str
    ppuzzles: Optional[list["ParagraphPuzzle"]]

class ParagraphPuzzle:
    paragraph: Optional["Paragraph"]
    cardpuzzle: Optional["CardPuzzle"]
    type: str
    quality: Optional[float]

    # TODO: how to save anwser?