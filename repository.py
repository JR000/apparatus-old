import dto
    
class Repository:
    def queryBooks(self, query: Logic) -> list[dto.Book]:
        raise NotImplementedError()
    def queryTokens(self, query: Logic) -> list[dto.Token]:
        ...
    def queryCards(self, query: Logic) -> list[dto.Card]:
        ...
    def querypParagraphs(self, query: Logic) -> list[dto.Paragraph]:
        ...
    def queryParagraphPuzzles(self, query: Logic) -> list[dto.ParagraphPuzzle]:
        ...
    def querySections(self, query: Logic) -> list[dto.Section]:
        ...
    def queryCardPuzzles(self, query: Logic) -> list[dto.CardPuzzle]:
        ...
    def queryCardSchedules(self, query: Logic) -> list[dto.CardSchedule]:
        ...
    def queryTokenSchedules(self, query: Logic) -> list[dto.TokenSchedule]:
        ...
    def queryTokenRequirements(self, query: Logic) -> list[dto.TokenRequirement]:
        ...


_repositories = {}
_default = None

def query_(table, logic, populates):
    ...

def register(registry: Repository, name: str):
    if not len(_repositories.keys()):
        _default = name
    _repositories[name] = registry

def unregister(registry: Repository):
    for key, reg in _repositories.items():
        if reg == registry:
            del _repositories[key]
            break
