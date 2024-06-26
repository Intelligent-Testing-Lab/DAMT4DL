import yaml # type: ignore

def read_yaml_config(file_path):
    """
    Reads the configuration file in YAML format
    """
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def init_conf(file_path):
    config = read_yaml_config(file_path)
    return config

if __name__ == '__main__':
    config = init_conf('../config_file/example.yaml')
    print(config['data'])
