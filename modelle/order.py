from functools import reduce
from modelle.identifiable import Identifiable
from repository.drink_repo import DrinkRepo
from repository.cooked_dish_repo import CookedDishRepo


class Order(Identifiable):
    def __init__(self, id, client_id, drinks_list, cooked_dishes_list, time_placed, expected_time, total_cost=None):
        super().__init__(id)
        self.client_id = client_id
        self.drinks_list = drinks_list
        self.cooked_dishes_list = cooked_dishes_list
        self.time_placed = time_placed
        self.expected_time = expected_time
        self.total_cost = self.calculate_cost() if total_cost is None else total_cost

    def calculate_cost(self):
        drinks_prices = []
        if self.drinks_list != ['']:
            repo = DrinkRepo('repository/data')
            for drink_id in self.drinks_list:
                item = repo.convert_from_str(self.get_item(drink_id, 'drinks.txt', repo))
                drinks_prices.append(item[0].price)

        cooked_dishes_prices = []
        if self.cooked_dishes_list != ['']:
            repo = CookedDishRepo('repository/data')
            for cooked_dish_id in self.cooked_dishes_list:
                item = repo.convert_from_str(self.get_item(cooked_dish_id, 'cooked_dishes.txt', repo))
                cooked_dishes_prices.append(item[0].price)

        order_prices = drinks_prices + cooked_dishes_prices
        return reduce(lambda a, b: a + int(b), order_prices, 0)

    def __string_receipt(self):
        string_receipt = f'Order ID = {self.id}\n' \
                         f'Client ID = {self.client_id}\n' \
                         f'============================\n'

        repo = DrinkRepo('repository/data')
        for id in self.drinks_list:
            string_receipt += f"{self.get_item(id, 'drinks.txt', repo)}\n"

        repo = CookedDishRepo('repository/data')
        for id in self.cooked_dishes_list:
            string_receipt += f"{self.get_item(id, 'cooked_dishes.txt', repo)}\n"

        string_receipt += f'============================\n' \
                          f'Total cost = {self.total_cost}\n' \
                          f'Time the order was placed: {self.time_placed}\n' \
                          f'Expected finish time: {self.expected_time}'
        return string_receipt

    def print_check(self):
        print(self.__string_receipt())

    def get_item(self, id, file, repo):
        item_list = repo.convert_to_str(repo.load(file))
        filtered_list = list(filter(lambda x: x.split('=')[1].split(',')[0] == id, item_list))
        return filtered_list[0]
