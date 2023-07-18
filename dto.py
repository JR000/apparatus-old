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
from typing import Any, Optional
import sys

"""
typing:

List == ([type])

"""

class CustomType:
    pass

class Scalar(CustomType):
    def equals(self, a):
        pass

class String(str, Scalar):
    def regex(self):
        return

class Int(int, Scalar):
    pass 

class Float(float, Scalar):
    pass 

class List(list):
    def has(self):
        pass

def get_type_from_annotation(annotation):
    # if is optional
    if hasattr(annotation, '__args__') \
        and len(annotation.__args__) == 2 \
        and annotation.__args__[-1] is type(None):
        return annotation.__args__[0]
    # else:
    return annotation

def dto(target):
    print(target.__module__)

    types_map: dict[str, str] = {}
    default_map: dict[str, object] = {}
    validators_map: dict[str, list] = {}
    for key, annotation in target.__annotations__.items():

        if not hasattr(target, key):
            print('continue', key)
            continue # TODO

        attr = getattr(target, key)
        if not isinstance(attr, tuple):
            raise TypeError() # TODO
        
        _default, validators = attr

        _type = get_type_from_annotation(annotation)
        types_map[key] = _type
        default_map[key] = _default
        validators_map[key] = validators
        if not isinstance(_type, str) and issubclass(_type, CustomType):
            setattr(target, key, _type())
    

    def is_attr_type_correct(name, value):
        _type = types_map[name]

        if isinstance(_type, str):
            module = sys.modules[target.__module__]
            if not hasattr(module, name):
                return False # TODO: change to Error
            _type = getattr(module, name)
            types_map[name] = _type            
        return isinstance(value, _type) or issubclass(_type, type(value))
    
    def clone(v):
        return v

    def __init__(self, **kwargs):
        for key, item in target.__annotations__.items():
            # add frozen 

            if key not in kwargs and key not in default_map:
                raise AttributeError(f"The attribute '{key}' has no default value")
            if key not in kwargs:
                setattr(self, key, clone(default_map[key]))
            else:
                setattr(self, key, kwargs[key])

    def __setattr__(self, name, value):
        if not is_attr_type_correct(name, value):
            raise TypeError() # TODO

        if name in validators_map:
            for validator in validators_map[name]:
                if not validator(value):
                    raise AttributeError(f"Validation failed for the attribute '{name}'")
        super(target, self).__setattr__(name, value)

    # TODO: add nested __repr__ ? 
    def __repr__(self):
        return f"{target.__name__}({', '.join([name +  '=' + val.__repr__() for name, val in self.__dict__.items()])})"

    target.__init__ = __init__
    target.__setattr__ = __setattr__
    target.__repr__ = __repr__

    return target   


def field(_default: Any = None, validators: list = []):
    return (
        _default,
        validators
    ) 

import typing
import dataclasses
dataclasses.dataclass

@dto
class Book:
    id: Optional[String] = field(_default="") # -> String() //default[id] = default
    title: String = field(_default="")
    card: "Card" = field()
    tokens: List["Token"]
    titles: List[String]

@dto
class Card:
    title: String = field()
print(Book(card=Card(title="i")))
Book.id.equals("w")
