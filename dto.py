from uuid import UUID
from dataclasses import dataclass
from typing import Generic, TypeVar, List, Any, Optional

T = TypeVar('T')
class Logic:
    ...
class SpreadableLogic:
    content: List[Logic]
    def __init__(self, *sublogic: List[Logic]):
        self.content = sublogic
class And(SpreadableLogic):
    ...
class Or(SpreadableLogic):
    ...
class Not(SpreadableLogic):
    ...

@dataclass
class FieldLogic(Logic):
    fieldname: str
    method: str
    content: Logic | Any


# TODO: typing check
class Searchable(Generic[T]):
    name: str
    def __init__(self, name: str = None):
        self.name = name
    def equals(self, value : T) -> FieldLogic:
        return FieldLogic(self.name, 'equals', value)
    def has(self, *sublogic) -> FieldLogic:
        return FieldLogic(self.name, 'has', sublogic)
    def regex(self, regex: str) -> FieldLogic:
        return FieldLogic(self.name, 'regex', regex)
    def among(self, values: list[Any]) -> FieldLogic:
        return FieldLogic(self.name, 'among', values)


def searchable(cls):
    for name, _ in cls.__annotations__.items():
        setattr(cls, name, Searchable(name=name))
    return cls

@searchable
@dataclass
class Book:
    id: UUID
    title: str
    author: str
    cards: Optional[list["Card"]]
    sections: Optional[list["Section"]]
    tokens: Optional["Token"]

@searchable
@dataclass
class Card:
    id: UUID
    type: str
    paragraphs: Optional[list["Paragraph"]]
    ordinal: Optional[int]
    parent: Optional["Section"]
    carried_tokens: Optional[list["Token"]]
    requirements: Optional[list["TokenRequirement"]]

@searchable
@dataclass
class Token:
    id: UUID
    title: str
    requirements: Optional[list["TokenRequirement"]]
    cards_carry: Optional[list["Card"]]

@searchable
@dataclass
class Paragraph:
    id: UUID
    type: str
    value: Any
    ordinal: Optional[int]

    card: Optional["Card"]
    parent: Optional["Paragraph"]
    subparagrpahs: Optional[list["Paragraph"]]

@searchable
@dataclass
class Section:
    id: UUID
    type: str
    ordinal: int

    subsections: Optional[list["Section"]]
    parent: Optional["Section"]
    cards: Optional[list["Card"]]

@searchable
@dataclass
class TokenRequirement:
    token: Optional["Token"]
    card: Optional["Card"]
    data: Optional[Any] # optional, потому что можно использовать и без: например, чтобы подчеркнуть наличие зависимости

@searchable
@dataclass
class TokenSchedule:
    token: Optional["Token"]
    system: str
    timastamp: Any # TODO: исправить типизацию
    puzzle: Optional["CardPuzzle"]
    data: Any # TODO: исправить типизацию

@searchable
@dataclass
class CardSchedule:
    card: Optional["Card"]
    system: str
    timastamp: Any # TODO: исправить типизацию
    puzzle: Optional["CardPuzzle"]
    data: Any # TODO: исправить типизацию

@searchable
@dataclass
class CardPuzzle:
    card: Optional["Card"]
    quality: float
    type: str
    ppuzzles: Optional[list["ParagraphPuzzle"]]

@searchable
@dataclass
class ParagraphPuzzle:
    paragraph: Optional["Paragraph"]
    cardpuzzle: Optional["CardPuzzle"]
    type: str
    quality: Optional[float]

    # TODO: how to save anwser?



"""
Двигаться в сторону:
разметка через простые типы
использование dataclass 
Searchable в качестве статической переменной
"""
