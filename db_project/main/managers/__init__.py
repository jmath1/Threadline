import importlib
import os

"""
probably not a great best practice to import everything 
programatically, but I am trying to
hit a deadline
"""
module_dir = os.path.dirname(__file__)
module_files = [f[:-3] for f in os.listdir(module_dir) if f.endswith('.py') and not f.startswith('__')]


for module_file in module_files:
    module = importlib.import_module(f'.{module_file}', __package__)
    classes = [cls for cls in module.__dict__.values() if isinstance(cls, type)]
    for cls in classes:
        globals()[cls.__name__] = cls

__all__ = [cls.__name__ for cls in globals().values() if isinstance(cls, type)]
