import os
from types import ModuleType
from typing import Iterator


class Handlers:
    base_path_handlers = ('controllers',)  # Ajustado para no repetir 'api'
    ignored = ('__init__.py', '__pycache__')

    @classmethod
    def __all_module_names(cls) -> list:
        # Obtener la ruta absoluta para los módulos dentro de 'api/controllers'
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Subimos un nivel para no duplicar 'api'
        handlers_path = os.path.join(base_dir, 'api', *cls.base_path_handlers)
        return list(
            filter(
                lambda module: module not in cls.ignored, os.listdir(handlers_path)
            )
        )

    @classmethod
    def __module_namespace(cls, handler_name: str) -> str:
        # Crear el namespace del módulo usando 'api.controllers'
        return 'api.%s' % ('.'.join(cls.base_path_handlers + (handler_name,)))

    @classmethod
    def iterator(cls) -> Iterator[ModuleType]:
        for module in cls.__all_module_names():
            import importlib
            handler = importlib.import_module(cls.__module_namespace(module[:-3]))
            yield handler

    @classmethod
    def modules(cls) -> map:
        return map(
            lambda module: cls.__module_namespace(module[:-3]), cls.__all_module_names()
        )
