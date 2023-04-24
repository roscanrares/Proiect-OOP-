from repository.data_repo import DataRepo
from modelle.drink import Drink


class DrinkRepo(DataRepo):
    def __init__(self, file):
        super().__init__(file)

    def convert_to_str(self, obj_list):
        def str_obj(obj):
            return f'Drink(id={obj.id}, name={obj.name}, portion_size={obj.portion_size}, price={obj.price}, alcohol_content={obj.alcohol_content})'

        return list(map(str_obj, obj_list))

    def convert_from_str(self, string_file):
        def create_drink(element):
            if element:
                element = element[:-1]
                attributes = element.split(',')

                id = attributes[0].split('=')[1]
                name = attributes[1].split('=')[1]
                portion_size = attributes[2].split('=')[1]
                price = attributes[3].split('=')[1]
                alcohol_content = attributes[4].split('=')[1]

                return Drink(id, name, portion_size, price, alcohol_content)

        string_list = string_file.split('\n')
        return list(map(create_drink, string_list))
