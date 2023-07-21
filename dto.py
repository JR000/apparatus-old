from uuid import UUID
from dataclasses import dataclass
from typing import Generic, TypeVar, List, Any, Optional, Union

T = TypeVar('T')
X = TypeVar('X')
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
class Searchable(Generic[X]):
    name: str
    def __init__(self, name: str = None):
        self.name = name
    def equals(self, value : X) -> FieldLogic:
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

QueryNode = Union[T, Searchable[T], Logic]

@searchable
@dataclass
class Book:
    id: QueryNode[UUID]
    title: QueryNode[str]
    author: QueryNode[str]
    cards: QueryNode[Optional[list["Card"]]]
    sections: QueryNode[Optional[list["Section"]]]
    tokens: QueryNode[Optional["Token"]]

@searchable
@dataclass
class Card:
    id: QueryNode[UUID]
    type: QueryNode[str]
    paragraphs: QueryNode[Optional[list["Paragraph"]]]
    ordinal: QueryNode[Optional[int]]
    parent: QueryNode[Optional["Section"]]
    carried_tokens: QueryNode[Optional[list["Token"]]]
    requirements: QueryNode[Optional[list["TokenRequirement"]]]

@searchable
@dataclass
class Token:
    id: QueryNode[UUID]
    title: QueryNode[str]
    requirements: QueryNode[Optional[list["TokenRequirement"]]]
    cards_carry: QueryNode[Optional[list["Card"]]]

@searchable
@dataclass
class Paragraph:
    id: QueryNode[UUID]
    type: QueryNode[str]
    value: QueryNode[Any]
    ordinal: QueryNode[Optional[int]]

    card: QueryNode[Optional["Card"]]
    parent: QueryNode[Optional["Paragraph"]]
    subparagrpahs: QueryNode[Optional[list["Paragraph"]]]

@searchable
@dataclass
class Section:
    id: QueryNode[UUID]
    type: QueryNode[str]
    ordinal: QueryNode[int]

    subsections: QueryNode[Optional[list["Section"]]]
    parent: QueryNode[Optional["Section"]]
    cards: QueryNode[Optional[list["Card"]]]

@searchable
@dataclass
class TokenRequirement:
    token: QueryNode[Optional["Token"]]
    card: QueryNode[Optional["Card"]]
    data: QueryNode[Optional[Any]] # optional, потому что можно использовать и без: например, чтобы подчеркнуть наличие зависимости

@searchable
@dataclass
class TokenSchedule:
    token: QueryNode[Optional["Token"]]
    system: QueryNode[str]
    timastamp: QueryNode[Any] # TODO: исправить типизацию
    puzzle: QueryNode[Optional["CardPuzzle"]]
    data: QueryNode[Any] # TODO: исправить типизацию

@searchable
@dataclass
class CardSchedule:
    card: QueryNode[Optional["Card"]]
    system: QueryNode[str]
    timastamp: QueryNode[Any] # TODO: исправить типизацию
    puzzle: QueryNode[Optional["CardPuzzle"]]
    data: QueryNode[Any] # TODO: исправить типизацию

@searchable
@dataclass
class CardPuzzle:
    card: QueryNode[Optional["Card"]]
    quality: QueryNode[float]
    type: QueryNode[str]
    ppuzzles: QueryNode[Optional[list["ParagraphPuzzle"]]]

@searchable
@dataclass
class ParagraphPuzzle:
    paragraph: QueryNode[Optional["Paragraph"]]
    cardpuzzle: QueryNode[Optional["CardPuzzle"]]
    type: QueryNode[str]
    quality: QueryNode[Optional[float]]

    # TODO: how to save anwser?

"""
Двигаться в сторону:
разметка через простые типы
использование dataclass 
Searchable в качестве статической переменной
"""
