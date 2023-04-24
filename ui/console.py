from controller.controller import Controller
from repository.client_repo import ClientRepo
from repository.drink_repo import DrinkRepo
from repository.cooked_dish_repo import CookedDishRepo
from repository.order_repo import OrderRepo
from datetime import datetime, timedelta


class Console:
    def __init__(self, controller=None):
        self.controller = controller

    def main_menu(self):
        def main_menu_ui():
            return """
                0 - Exit
                1 - New order
                2 - Edit data
            """

        while True:
            print(main_menu_ui())
            opt = input('Select = ')

            if opt == '1':
                self.order_menu()

            if opt == '2':
                self.edit_menu()

            if opt == '0':
                break

    def order_menu(self):
        def order_menu_ui():
            return """
                0 - Exit
                1 - Print menu items
                2 - Add item to order
                3 - Add client info
                4 - Finish order
            """

        id = input('Order ID = ')
        client_id = None
        drinks_list = []
        cooked_dishes_list = []

        while True:
            print(order_menu_ui())
            opt = input('Select = ')

            if opt == '1':
                self.controller = Controller(DrinkRepo('repository/data'))
                print(self.controller.repo.read_file('drinks.txt'))

                self.controller = Controller(CookedDishRepo('repository/data'))
                print(self.controller.repo.read_file('cooked_dishes.txt'))

            if opt == '2':
                new_drinks_list, new_cooked_dishes_list = self.add_items_to_order_menu()
                drinks_list += new_drinks_list
                cooked_dishes_list += new_cooked_dishes_list

            if opt == '3':
                client_id = self.add_client_info_menu()

            if opt == '4':
                if client_id == None or not drinks_list + cooked_dishes_list:
                    print('Incomplete information:')
                    print('No client info registered') if client_id == None else print('No items added to order')
                else:
                    time_placed = datetime.now()
                    self.controller = Controller(CookedDishRepo('repository/data'))
                    hours, minutes = self.controller.calculate_time(cooked_dishes_list)
                    expected_time = (time_placed + timedelta(hours=hours, minutes=minutes)).strftime('%H:%M')
                    time_placed = time_placed.strftime('%H:%M')

                    self.controller = Controller(OrderRepo('repository/data'))
                    order = self.controller.generate_order(id, client_id, drinks_list, cooked_dishes_list, time_placed,
                                                           expected_time)
                    order.print_check()

            if opt == '0':
                break

    def add_client_info_menu(self):
        def add_client_info_ui():
            return """
                0 - Exit
                1 - Add new client to order
                2 - Add existing client to order
            """

        self.controller = Controller(ClientRepo('repository/data'))
        while True:
            print(add_client_info_ui())
            opt = input('Select = ')

            if opt == '1':
                id = input('ID = ')
                name = input('Name = ')
                address = input('Address = ')
                self.controller.add_client(id, name, address)
                return id

            if opt == '2':
                client_info = input('Enter client info (name/address) = ')
                id, nr_app = self.controller.search_client_id(client_info)
                if nr_app == 1:
                    return id
                elif nr_app == 0:
                    print('No client with such info exists, try again.')
                else:
                    print(f'{nr_app} clients with this info exist, try again with more secific info.')

            if opt == '0':
                break

    def add_items_to_order_menu(self):
        def add_items_to_order_ui():
            return """
                0 - Exit
                1 - Add drinks
                2 - Add cooked dishes
            """

        drinks_list = []
        cooked_dishes_list = []
        while True:
            print(add_items_to_order_ui())
            opt = input('Select = ')

            if opt == '1':
                self.controller = Controller(DrinkRepo('repository/data'))
                id = input('Enter the ID = ')
                if self.controller.search_item(id, opt):
                    drinks_list.append(id)
                else:
                    print(f'The item with the ID:{id} does not exist')

            if opt == '2':
                self.controller = Controller(CookedDishRepo('repository/data'))
                id = input('Enter the ID = ')
                if self.controller.search_item(id, opt):
                    cooked_dishes_list.append(id)
                else:
                    print(f'The item with the ID:{id} does not exist')

            if opt == '0':
                break

        return drinks_list, cooked_dishes_list

    def edit_menu(self):
        def edit_menu_ui():
            return """
                0 - Exit
                1 - Edit drinks
                2 - Edit cooked dishes
                3 - Edit clients
            """

        while True:
            print(edit_menu_ui())
            opt = input('Select = ')

            if opt == '1':
                self.edit_drinks_menu()

            if opt == '2':
                self.edit_cooked_dishes_menu()

            if opt == '3':
                self.edit_client_menu()

            if opt == '0':
                break

    def edit_drinks_menu(self):
        def edit_drinks_ui():
            return """
                0 - Exit
                1 - Add drink
                2 - Print drinks
                3 - Edit drink
                4 - Remove drink
            """

        self.controller = Controller(DrinkRepo('repository/data'))
        while True:
            print(edit_drinks_ui())
            opt = input('Select = ')

            if opt == '1':
                id = input('ID = ')
                name = input('Name = ')
                portion_size = input('Portion size = ')
                price = input('Price = ')
                alcohol_content = input('Alcohol content = ')
                self.controller.add_drink(id, name, portion_size, price, alcohol_content)

            if opt == '2':
                print(self.controller.repo.read_file('drinks.txt'))

            if opt == '3':
                edit_id = input('Enter the ID of the drink you want to edit = ')
                self.controller.edit_drink(edit_id)

            if opt == '4':
                delete_id = input('Enter the ID of the drink you want to delete = ')
                self.controller.delete_entry(delete_id, 'drinks.txt')

            if opt == '0':
                break

    def edit_cooked_dishes_menu(self):
        def edit_cooked_dishes_ui():
            return """
                0 - Exit
                1 - Add cooked dish
                2 - Print cooked dishes
                3 - Edit cooked dish
                4 - Remove cooked dish
            """

        self.controller = Controller(CookedDishRepo('repository/data'))
        while True:
            print(edit_cooked_dishes_ui())
            opt = input('Select = ')

            if opt == '1':
                id = input('ID = ')
                name = input('Name = ')
                portion_size = input('Portion size = ')
                price = input('Price = ')
                prep_time = input('Preparation time = ')
                self.controller.add_cooked_dish(id, name, portion_size, price, prep_time)

            if opt == '2':
                print(self.controller.repo.read_file('cooked_dishes.txt'))

            if opt == '3':
                edit_id = input('Enter the ID of the cooked dish you want to edit = ')
                self.controller.edit_cooked_dish(edit_id)

            if opt == '4':
                delete_id = input('Enter the ID of the cooked dish you want to delete = ')
                self.controller.delete_entry(delete_id, 'cooked_dishes.txt')

            if opt == '0':
                break

    def edit_client_menu(self):
        def edit_client_ui():
            return """
                0 - Exit
                1 - Add client
                2 - Print clients
                3 - Edit client
                4 - Remove client
            """

        self.controller = Controller(ClientRepo('repository/data'))
        while True:
            print(edit_client_ui())
            opt = input('Select = ')

            if opt == '1':
                id = input('ID = ')
                name = input('Name = ')
                address = input('Address = ')
                self.controller.add_client(id, name, address)

            if opt == '2':
                print(self.controller.repo.read_file('clients.txt'))

            if opt == '3':
                print('Enter new info:')
                new_name = input('New name = ')
                new_address = input('New address = ')

                edit_id = input('Enter the ID of the client you want to edit = ')
                self.controller.edit_client(edit_id, new_name, new_address)

            if opt == '4':
                delete_id = input('Enter the ID of the client you want to delete = ')
                self.controller.delete_entry(delete_id, 'clients.txt')

            if opt == '0':
                break
