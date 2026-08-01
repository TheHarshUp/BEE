import importlib
import pkgutil

import bee.commands


def load_commands():
    commands = {}

    for _, module_name, _ in pkgutil.iter_modules(
        bee.commands.__path__
    ):
        module = importlib.import_module(
            f"bee.commands.{module_name}"
        )

        if hasattr(module, "run"):
            commands[f"/{module_name}"] = module.run

    return commands