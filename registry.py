class Registry:
    def get(self, field: str):
        raise NotImplementedError()
    def set(self, field: str, value):
        raise NotImplementedError()

_registries: dict[str, Registry] = {}
_default = None

def get(field: str, registry_id=None):
    if registry_id == None: _registry_id = _default
    return _registries[_registry_id].get(field)

def set(field: str, value, registry_id=None):
    if registry_id == None: _registry_id = _default
    _registries[_registry_id].set(field, value)

def register(registry: Registry, name: str):
    if not len(_registries.keys()):
        _default = name
    _registries[name] = registry

def unregister(registry: Registry):
    for key, reg in _registries.items():
        if reg == registry:
            del _registries[key]
            break