class Product:
    """Represents a single product and manages its own state.

    Responsibility (SRP): store one product's information and control
    how that information changes. It does not read input, print menus,
    touch files or manage other products.
    """

    def __init__(self, product_id, name, price, stock):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        # Double underscore marks these as private: outside code should
        # use the public methods below instead of changing them directly.
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        # The Product decides what counts as a valid stock level.
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = int(quantity)

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
