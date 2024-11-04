from datetime import datetime


class Ebook:
    def __init__(self, title, author, publicationDate, genre, price):
        self.__title = title
        self.__author = author
        self.__publicationDate = publicationDate
        self.__genre = genre
        self.__price = price

    def get_title(self):
        return self.__title

    def get_price(self):
        return self.__price

    def __str__(self):
        return f"Ebook(\ntitle={self.__title},\nauthor={self.__author},\nprice={self.__price})"


class Catalog:
    def __init__(self):
        self.__ebooks = []

    def add_ebook(self, ebook):
        self.__ebooks.append(ebook)

    def remove_ebook(self, title):
        self.__ebooks = list(filter(lambda ebook: ebook.get_title() != title, self.__ebooks))

    def search_ebook(self, title):
        for ebook in self.__ebooks:
            if ebook.get_title() == title:
                return ebook
        return None

    def list_ebooks(self):
        return self.__ebooks

    def __str__(self):
        return '\n'.join(str(ebook) for ebook in self.__ebooks)


class Customer:
    def __init__(self, name, contact_info):
        self.__name = name
        self.__contact_info = contact_info
        self.__shopping_cart = ShoppingCart()

    def browse_catalog(self, catalog):
        return catalog.list_ebooks()

    def add_to_cart(self, ebook):
        self.__shopping_cart.add_item(ebook)

    def order(self):
        order = Order(self, self.__shopping_cart)
        invoice = order.generate_invoice()
        self.__shopping_cart.clear_cart()
        return invoice

    def __str__(self):
        return f"Customer(\nname={self.__name},\ncontact_info={self.__contact_info})"


class RoyaltyProgram(Customer):
    def __init__(self, name, contact_info):
        super().__init__(name, contact_info)
        self.__discount = 0.10

    def apply_discount(self, total):
        return total * (1 - self.__discount)

    def __str__(self):
        return f"RoyaltyProgram({super().__str__()})"


class ShoppingCart:
    def __init__(self):
        self.__items = []

    def add_item(self, ebook):
        self.__items.append(ebook)

    def remove_item(self, title):
        self.__items = list(filter(lambda item: item.get_title() != title, self.__items))

    def get_items(self):
        return self.__items

    def clear_cart(self):
        self.__items.clear()

    def __str__(self):
        return '\n'.join(str(item) for item in self.__items)


class Order:
    VAT = 0.08

    def __init__(self, customer, shopping_cart):
        self.__customer = customer
        self.__shopping_cart = shopping_cart
        self.__order_date = datetime.now()
        self.__items = shopping_cart.get_items()
        self.__total_amount = self.calculate_total()

    def calculate_total(self):
        total = sum(ebook.get_price() for ebook in self.__shopping_cart.get_items())
        total += total * self.VAT
        if isinstance(self.__customer, RoyaltyProgram):
            total = self.__customer.apply_discount(total)
        return total

    def generate_invoice(self):
        items_str = '\n'.join(str(item) for item in self.__shopping_cart.get_items())
        return f"Invoice for {self.__customer},\norder date: {self.__order_date.strftime("%Y-%m-%d %H:%M:%S")},\nItems:\n{items_str}\nTotal: {self.calculate_total():.2f}"

    def __str__(self):
        return f"Order(customer=\n{self.__customer},\norder date: {self.__order_date.strftime("%Y-%m-%d %H:%M:%S")},\ntotal={self.calculate_total():.2f})"


# Testing example
if __name__ == "__main__":
    ebook1 = Ebook("Treasure Island", "Robert Louis Stevenson", "1883-11-14", "Adventure fiction", 100)
    ebook2 = Ebook("Alice's Adventures in Wonderland", "Lewis Carroll", "1865-11", "Portal fantasy", 75)

    catalog = Catalog()
    catalog.add_ebook(ebook1)
    catalog.add_ebook(ebook2)

    customer = Customer("Waad Alhefeiti", "202217028@zu.ac.ae")
    print("Catalog:")
    print(catalog)


    customer.add_to_cart(ebook1)
    customer.add_to_cart(ebook2)
    print("Order Invoice:")
    print(customer.order())
