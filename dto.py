from dataclasses import dataclass
from typing import Generic, TypeVar, List, Any, Optional, Union, Dict
from datetime import datetime

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

QueryNode = Union[Optional[T], Searchable[T], Logic]

class DTO:
    ...
    
@searchable
@dataclass
class Book(DTO):
    id: QueryNode[int]
    title: QueryNode[str]
    author: QueryNode[str]
    cards: QueryNode[list["Card"]]
    sections: QueryNode[list["Section"]]
    tokens: QueryNode[list["Token"]]
    
@searchable
@dataclass
class Section(DTO):
    id: QueryNode[int]
    title: QueryNode[str]
    type: QueryNode[str]
    ordinal: QueryNode[int]
    book: QueryNode["Book"]
    parent: QueryNode["Section"]
    subsections: QueryNode[Dict[int, "Section"]]
    cards: QueryNode[list["Card"]]
    
@searchable
@dataclass
class Card(DTO):
    id: QueryNode[int]
    type: QueryNode[str]
    title: QueryNode[str]
    book: QueryNode["Book"]
    section: QueryNode["Section"]
    paragraphs: QueryNode[list["Paragraph"]]
    cardpuzzles: QueryNode[list["CardPuzzle"]]
    cardschedules: QueryNode[list["CardSchedule"]]
    requirements: QueryNode[list["TokenRequirement"]]
    carried_tokens: QueryNode[list["Token"]]
    
@searchable
@dataclass
class Paragraph(DTO):
    id: QueryNode[int]
    card: QueryNode["Card"]
    type: QueryNode[str]
    value: QueryNode[str]
    parent: QueryNode["Paragraph"]
    subparagraphs: QueryNode[Dict[int, "Paragraph"]]
    paragraphpuzzles: QueryNode[list["ParagraphPuzzle"]]
    
@searchable
@dataclass
class Token(DTO):
    id: QueryNode[int]
    title: QueryNode[str]
    book: QueryNode["Book"]
    tokenschedules: QueryNode[list["TokenSchedule"]]
    requirements: QueryNode[list["TokenRequirement"]]
    carriers: QueryNode[list["Card"]]
    
@searchable
@dataclass
class CardPuzzle(DTO):
    id: QueryNode[int]
    type: QueryNode[str]
    quality: QueryNode[float]
    timestamp: QueryNode[datetime]
    card: QueryNode["Card"]
    paragraphpuzzles: QueryNode["ParagraphPuzzle"]
    cardschedules: QueryNode[list["CardSchedule"]]
    tokenschedules: QueryNode[list["TokenSchedule"]]
    
@searchable
@dataclass
class ParagraphPuzzle(DTO):
    id: QueryNode[int]
    type: QueryNode[str]
    quality: QueryNode[float]
    paragraph: QueryNode["Paragraph"]
    cardpuzzle: QueryNode["CardPuzzle"]
    
@searchable
@dataclass
class CardSchedule(DTO):
    id: QueryNode[int]
    system: QueryNode[str]
    timestamp: QueryNode[datetime]
    card: QueryNode["Card"]
    cardpuzzle: QueryNode["CardPuzzle"]

@searchable
@dataclass
class TokenSchedule(DTO):
    id: QueryNode[int]
    system: QueryNode[str]
    timestamp: QueryNode[datetime]
    token: QueryNode["Token"]
    cardpuzzle: QueryNode["CardPuzzle"]
    
@searchable
@dataclass
class TokenRequirement(DTO):
    token: QueryNode["Token"]
    card: QueryNode["Card"]
