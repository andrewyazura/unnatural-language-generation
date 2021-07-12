import yaml


def load_yaml(filename):
    with open(filename, 'r') as stream:
        file = yaml.safe_load(stream)
    return file
