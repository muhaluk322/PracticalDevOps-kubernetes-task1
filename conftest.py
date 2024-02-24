import yaml

DATA = None


def pytest_addoption(parser):
    parser.addoption("--files", action="store")


def pytest_configure(config):
    global DATA
    files = config.option.files.split(",")
    DATA = []
    for file in files:
        with open(file) as f:
            DATA.extend(list(yaml.load_all(f, yaml.SafeLoader)))