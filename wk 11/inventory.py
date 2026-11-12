from product import Product

LINE = "-" * 48


class Inventory:
    """Manages a collection of Product objects.

    Responsibility (SRP): store, add, search and display products.
    Each Product still manages its own state; the Inventory only
    looks after the collection.
    """

    # Lab 8, sections 3 and 5: aggregation of independently created Products.
    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:
        """Return a copy containing the same Product objects (not new products)."""
        return list(self.__products)

    def add_product(self, product: Product) -> bool:
        # Product IDs must be unique, so refuse duplicates.
        if self.search_product(product.get_product_id()):
            return False
        self.__products.append(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        """Keep the Lab 7 menu API while exposing the Lab 8 find method."""
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def update_stock(self, product_id: str, quantity: int) -> bool:
        product = self.search_product(product_id)
        if not product:
            return False
        # Ask the Product to change its own stock rather than editing it here.
        product.update_stock(quantity)
        return True

    def get_products(self) -> list[Product]:
        # Return a copy so outside code cannot change the internal list.
        return list(self.__products)

    def display_all_products(self) -> None:
        """Lab 8, sections 6.1 and 7: one loop uses the Product abstraction."""
        print("\nCurrent Inventory")
        print(LINE)
        if not self.__products:
            print("Inventory is empty.")
        for product in self.__products:
            product.display_information()
            print(product.get_fulfilment_info())
        print(LINE)

    def display_all(self) -> None:
        self.display_all_products()
