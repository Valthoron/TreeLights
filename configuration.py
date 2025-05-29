import yaml


class Configuration:
    pin: str = "D12"
    pixel_order: str = "RGB"
    animation_duration: int = 60
    playlist: set[str] = set([])


def _read_property(configuration: Configuration, attribute_name: str, document, item_name: str):
    # This is a brute-force way to load, but that's fine for this project.
    if not hasattr(configuration, attribute_name):
        return

    if not item_name in document:
        return

    setattr(configuration, attribute_name, type(getattr(configuration, attribute_name))(document[item_name]))


def load_configuration(yaml_file_name: str) -> Configuration:
    configuration = Configuration()

    with open(yaml_file_name, "r", encoding="utf-8") as config_file_stream:
        document = yaml.safe_load(config_file_stream)

        _read_property(configuration, "pin", document, "Pin")
        _read_property(configuration, "pixel_order", document, "PixelOrder")
        _read_property(configuration, "animation_duration", document, "AnimationDuration")
        _read_property(configuration, "playlist", document, "Playlist")

    return configuration
