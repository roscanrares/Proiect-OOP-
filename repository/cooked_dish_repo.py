from repository.data_repo import DataRepo
from modelle.cooked_dish import CookedDish


class CookedDishRepo(DataRepo):
    def __init__(self, file):
        super().__init__(file)

    def convert_to_str(self, obj_list):
        def str_obj(obj):
            return f'CookedDish(id={obj.id}, name={obj.name}, portion_size={obj.portion_size}, price={obj.price}, prep_time={obj.prep_time})'

        return list(map(str_obj, obj_list))

    def convert_from_str(self, string_file):
        def create_cooked_dish(element):
            if element:
                element = element[:-1]
                attributes = element.split(',')

                id = attributes[0].split('=')[1]
                name = attributes[1].split('=')[1]
                portion_size = attributes[2].split('=')[1]
                price = attributes[3].split('=')[1]
                prep_time = attributes[4].split('=')[1]

                return CookedDish(id, name, portion_size, price, prep_time)

        string_list = string_file.split('\n')
        return list(map(create_cooked_dish, string_list))
