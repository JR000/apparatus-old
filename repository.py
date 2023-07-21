import dto

class Repository:
    def query(self, table: type, logic: dto.Logic, populates: dto.DTO = None) -> list[dto.DTO]:
        raise NotImplementedError()

_repositories: dict[str, Repository] = {}
_default: str = ""

def query(table: type, logic: dto.Logic, populates: dto.DTO = None, repository: str = _default) -> list[dto.DTO]:
    if repository not in _repositories:
        raise KeyError("Repository of the key \"{repository}\" was not found")
    return _repositories[repository].query(table, logic, populates)

def register(registry: Repository, name: str):
    if not len(_repositories.keys()):
        _default = name
    _repositories[name] = registry

def unregister(registry: Repository):
    for key, reg in _repositories.items():
        if reg == registry:
            del _repositories[key]
            break
