class DataRepo:
    def __init__(self, file):
        self.file = file

    def save(self, obj_list, obj_file):
        with open(f'{self.file}/{obj_file}', 'w') as f:
            for i, obj in enumerate(obj_list):
                f.write(str(obj))
                if i < len(obj_list) - 1:
                    f.write('\n')

    def load(self, obj_file):
        with open(f'{self.file}/{obj_file}', 'r') as f:
            list_strings = f.read()
        return self.convert_from_str(list_strings)

    def read_file(self, obj_file):
        with open(f'{self.file}/{obj_file}', 'r') as f:
            string_file = f.read()
        return string_file

    def write_to_file(self, string_to_file, obj_file):
        with open(f'{self.file}/{obj_file}', 'w') as f:
            f.write(string_to_file)

    def convert_to_str(self, obj_list):
        pass

    def convert_from_str(self, obj_string):
        pass
