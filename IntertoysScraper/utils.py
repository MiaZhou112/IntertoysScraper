import yaml

def read_config(config_path):
    with open(config_path, "r") as f:
        try:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        except yaml.YAMLError as e:
            print(e)
    return cfg

