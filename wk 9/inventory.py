LINE = "-" * 48


class Inventory:
    """Manages a collection of Product objects.

    Responsibility (SRP): store, add, search and display products.
    Each Product still manages its own state; the Inventory only
    looks after the collection.
    """

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        # Product IDs must be unique, so refuse duplicates.
        if self.search_product(product.get_product_id()):
            return False
        self.__products.append(product)
        return True

    def search_product(self, product_id):
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def update_stock(self, product_id, quantity):
        product = self.search_product(product_id)
        if not product:
            return False
        # Ask the Product to change its own stock rather than editing it here.
        product.update_stock(quantity)
        return True

    def get_products(self):
        # Return a copy so outside code cannot change the internal list.
        return list(self.__products)

    def display_all(self):
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
        print(LINE)
