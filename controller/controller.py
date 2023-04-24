from modelle.client import Client
from modelle.cooked_dish import CookedDish
from modelle.drink import Drink
from modelle.order import Order


def search_index(search_list, item):
    for i, obj in enumerate(search_list):
        if obj == item:
            return i


class Controller:
    def __init__(self, repo):
        self.repo = repo

    def add_client(self, id, name, address):
        obj_list = self.repo.load('clients.txt')
        obj_list.append(Client(id, name, address))
        self.repo.save(self.repo.convert_to_str(obj_list), 'clients.txt')

    def add_drink(self, id, name, portion_size, price, alcohol_content):
        obj_list = self.repo.load('drinks.txt')
        obj_list.append(Drink(id, name, portion_size, price, alcohol_content))
        self.repo.save(self.repo.convert_to_str(obj_list), 'drinks.txt')

    def add_cooked_dish(self, id, name, portion_size, price, prep_time):
        obj_list = self.repo.load('cooked_dishes.txt')
        obj_list.append(CookedDish(id, name, portion_size, price, prep_time))
        self.repo.save(self.repo.convert_to_str(obj_list), 'cooked_dishes.txt')

    def edit_client(self, edit_id, new_name, new_address):
        client_list = self.repo.convert_to_str(self.repo.load('clients.txt'))
        filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == edit_id, client_list))

        if filtered_list:
            index = search_index(client_list, filtered_list[0])
            client_list[index] = f'Client(id={edit_id}, name={new_name}, address={new_address})'
            self.repo.save(client_list, 'clients.txt')
        else:
            print(f'The client with the ID: {edit_id} does not exist')

    def edit_drink(self, edit_id):
        drinks_list = self.repo.convert_to_str(self.repo.load('drinks.txt'))
        filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == edit_id, drinks_list))

        if filtered_list:
            print('Enter new info:')
            new_name = input('New name = ')
            new_portion_size = input('New portion size = ')
            new_price = input('New price = ')
            new_alcohol_content = input('New alcohol content = ')

            index = search_index(drinks_list, filtered_list[0])
            drinks_list[
                index] = f'Drink(id={edit_id}, name={new_name}, portion_size={new_portion_size}, price={new_price}, alcohool_content={new_alcohol_content})'
            self.repo.save(drinks_list, 'drinks.txt')
        else:
            print(f'The drink with the ID: {edit_id} does not exist')

    def edit_cooked_dish(self, edit_id):
        cooked_dishes_list = self.repo.convert_to_str(self.repo.load('cooked_dishes.txt'))
        filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == edit_id, cooked_dishes_list))

        if filtered_list:
            print('Enter new info:')
            new_name = input('New name = ')
            new_portion_size = input('New portion size = ')
            new_price = input('New price = ')
            new_prep_time = input('New preparation time = ')

            index = search_index(cooked_dishes_list, filtered_list[0])
            cooked_dishes_list[
                index] = f'CookedDish(id={edit_id}, name={new_name}, portion_size={new_portion_size}, price={new_price}, prep_time={new_prep_time})'
            self.repo.save(cooked_dishes_list, 'cooked_dishes.txt')
        else:
            print(f'The cooked dish with the ID: {edit_id} does not exist')

    def delete_entry(self, delete_id, file):
        entry_list = self.repo.convert_to_str(self.repo.load(file))
        filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == delete_id, entry_list))

        if filtered_list:
            entry_list.remove(filtered_list[0])
            self.repo.save(entry_list, file)
        else:
            item = file[:-6].replace("_", " ") if file == 'cooked_dishes.txt' else file[:-5]
            print(f'The {item} with the ID: {delete_id} does not exist')

    def generate_order(self, id, client_id, drinks_list, cooked_dishes_list, time_placed, expected_time):
        order = Order(id, client_id, drinks_list, cooked_dishes_list, time_placed, expected_time)
        order_list = self.repo.convert_to_str(self.repo.load('orders.txt'))
        order_list.append(self.repo.convert_to_str([order])[0])
        self.repo.save(order_list, 'orders.txt')
        return order

    def search_item(self, id, item_type):
        if item_type == '1':
            drinks_list = self.repo.convert_to_str(self.repo.load('drinks.txt'))
            filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == id, drinks_list))
        else:
            cooked_dishes_list = self.repo.convert_to_str(self.repo.load('cooked_dishes.txt'))
            filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == id, cooked_dishes_list))
        return True if len(filtered_list) == 1 else False

    def search_client_id(self, client_info):
        client_info = client_info.lower()
        client_list = self.repo.convert_to_str(self.repo.load('clients.txt'))

        filtered_name_list = list(
            filter(lambda x: client_info in x.split('=')[2].split(',')[0].lower(), client_list))
        filtered_address_list = list(
            filter(lambda x: client_info in x.split('=')[3].split(',')[0].lower(), client_list))
        filtered_list = filtered_address_list + filtered_name_list

        rez = []
        for el in filtered_list:
            if el not in rez:
                rez.append(el)

        if len(rez) == 0:
            return None, 0

        rez = '\n'.join(rez)
        rez = self.repo.convert_from_str(rez)
        return (rez[0].id, 1) if len(rez) == 1 else (None, len(rez))

    def calculate_time(self, lista):
        def get_item(id):
            item_list = self.repo.convert_to_str(self.repo.load('cooked_dishes.txt'))
            filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == id, item_list))
            return self.repo.convert_from_str(filtered_list[0])[0]

        minutes = 0
        for id in lista:
            minutes += int(get_item(id).prep_time)

        hours = minutes // 60
        minutes = minutes % 60

        return hours, minutes
