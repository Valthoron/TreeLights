import importlib.util
import os
import sys

from neopixel import NeoPixel

from lamps import Lamps


class Animation():
    name: str

    def initialize(self, lamps: Lamps):
        pass

    def update(self, lamps: Lamps, pixels: NeoPixel, time: float, delta_time: float):
        pass


def _files_in(path):
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            yield name


def _load_animation(name: str) -> Animation | None:
    full_name = f"animations.{name}"
    resolved_name = importlib.util.resolve_name(full_name, None)
    spec = importlib.util.find_spec(resolved_name)

    if spec is None:
        return None

    if spec.loader is None:
        return None

    lib = importlib.util.module_from_spec(spec)
    sys.modules[resolved_name] = lib
    spec.loader.exec_module(lib)

    instantiate = getattr(lib, "instantiate")
    return instantiate()


def load_animations() -> dict[str, Animation]:
    animations: dict[str, Animation] = {}

    for file_name in _files_in("animations"):
        if not file_name.endswith(".py"):
            continue

        animation_name = file_name.replace(".py", "")

        animation = _load_animation(animation_name)

        if animation is None:
            continue

        animation.name = animation_name
        animations[animation_name] = animation
        print(f">  {animation_name}")

    return animations
