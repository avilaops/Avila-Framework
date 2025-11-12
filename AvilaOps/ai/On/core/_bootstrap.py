"""Runtime helpers for ensuring the local 'on' namespace resolves correctly."""

from __future__ import annotations

import sys
import types
from importlib.machinery import ModuleSpec
from pathlib import Path


def ensure_on_namespace() -> None:
    """Ensure the in-repo 'on' package is discoverable on sys.path."""
    base_dir = Path(__file__).resolve().parents[1]
    base_str = str(base_dir)
    module_name = "on"

    if base_str not in sys.path:
        sys.path.insert(0, base_str)

    package = sys.modules.get(module_name)

    if package is None or getattr(package, "__path__", None) is None:
        package = types.ModuleType(module_name)
        sys.modules[module_name] = package

    existing_paths = list(getattr(package, "__path__", []))
    if base_str not in existing_paths:
        existing_paths.insert(0, base_str)
    package.__path__ = existing_paths
    package.__package__ = module_name

    spec = getattr(package, "__spec__", None)
    if not isinstance(spec, ModuleSpec) or not spec.submodule_search_locations:
        spec = ModuleSpec(module_name, loader=None, is_package=True)
        spec.submodule_search_locations = list(existing_paths)
        package.__spec__ = spec
    else:
        merged_locations = list(existing_paths)
        spec.submodule_search_locations = merged_locations
