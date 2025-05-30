import yaml


def load_configuration(yaml_file_name: str):
    with open(yaml_file_name, "r", encoding="utf-8") as config_file_stream:
        return yaml.safe_load(config_file_stream)

    return {}
