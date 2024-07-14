import yaml # type: ignore

class Config:
    def __init__(self, subject_name, original_path, mutations, mode, criterion, workers_num=1):
        self.subject_name = subject_name
        self.original_path = original_path
        self.mutations = mutations
        self.mode = mode
        self.criterion = criterion
        self.workers_num = workers_num
   
    @staticmethod
    def from_yaml(file_path):
        with open(file_path, 'r') as file:
           data = yaml.safe_load(file)
           return Config(**data)

if __name__ == '__main__':
    conf = Config.from_yaml('../config_file/example.yaml')
    print(conf.mutations)
    
