import config
from typing import List, Any, Optional, Dict
import json
from dataclasses import dataclass
import os
import importlib.util
import sys

@dataclass
class ExtensionIdentifier:
    id: str
    alias: str
@dataclass
class ExtensionSettingsRecord:
    alias: str
    type: str
    default: Any
@dataclass
class ExtensionRecord:
    identifier: ExtensionIdentifier
    title: str
    path: str
    settings: List[ExtensionSettingsRecord]
    def __post_init__(self):
        self.settings = [ExtensionSettingsRecord(**item) for item in self.settings]
        self.identifier = ExtensionIdentifier(**self.identifier)
        self.path = os.path.join(config.EXTENSIONS_FOLDER, self.path)
@dataclass
class ExtensionsFile:
    extensions: Dict[str, ExtensionRecord]
    def __post_init__(self):
        for extension_id, value in self.extensions.items():
            # TODO: check if key == record.identifier.id
            # TODO: check if record.identifier.alias is unique
            self.extensions[extension_id] = ExtensionRecord(**value)

_loadedExtensionAliases: list[str] = []
_records: dict[str, ExtensionRecord] = dict()

def loadInstalled():
    global _records
    final_dict: dict[str, ExtensionRecord] = {}
    with open(config.EXTENSIONS_JSON, 'r') as file:
        extensionsFile = ExtensionsFile(**json.load(file))
    for id, record in extensionsFile.extensions.items():
        try:
            _loadExtension(record)
            print(f'Extension "{record.identifier.alias}" was loaded')
        except:
            print(f'[ERROR] Extension "{record.identifier.alias}" was not loaded')
            continue
        
        final_dict[id] = record
            
    _records = final_dict
    _initializeAll()
    _updateJson()
        
def _updateJson():
    global _records
    print(_records)

def _loadExtension(record: ExtensionRecord):
    if not os.path.exists(record.path):
        raise FileNotFoundError(f'File "{record.path}" for the extension "{record.title}" was not found')
    # TODO: if alias is not unquie
    spec = importlib.util.spec_from_file_location(record.identifier.alias, record.path)
    print(record.path)
    sys.modules[record.identifier.alias] = importlib.util.module_from_spec(spec)
    module = sys.modules[record.identifier.alias]
    spec.loader.exec_module(module)
    
def _initializeAll():
    global _records
    for id, record in _records.items():
        module = sys.modules[record.identifier.alias]
        has_initialize = hasattr(module, 'initialize')
        print(has_initialize)
        if has_initialize:
            initalize = getattr(module, 'initialize')
            if isinstance(initalize, function):
                initalize()
