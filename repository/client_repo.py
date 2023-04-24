from repository.data_repo import DataRepo
from modelle.client import Client


class ClientRepo(DataRepo):
    def __init__(self, file):
        super().__init__(file)

    def convert_to_str(self, obj_list):
        def str_obj(obj):
            return f'Client(id={obj.id}, name={obj.name}, address={obj.address})'

        return list(map(str_obj, obj_list))

    def convert_from_str(self, string_file):
        def create_client(element):
            element = element[:-1]
            attributes = element.split(',')

            id = attributes[0].split('=')[1]
            name = attributes[1].split('=')[1]
            address = attributes[2].split('=')[1]

            return Client(id, name, address)

        string_list = string_file.split('\n')
        return list(map(create_client, string_list))
