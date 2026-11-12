from abc import ABC, abstractmethod
from typing import NotRequired, TypedDict
from supplier import Supplier, SupplierRecord


class ProductRecord(TypedDict):
    """Typed JSON boundary, including optional subtype and legacy fields."""
    id: str
    name: str
    price: float
    stock: int
    supplier: NotRequired[SupplierRecord]
    type: NotRequired[str]
    weight: NotRequired[float]
    download_size: NotRequired[float]
    duration_months: NotRequired[int]


class Product(ABC):
    """Abstract base class holding what every type of product has in common.

    Responsibility (SRP): store one product's common information and control
    how that information changes. It does not read input, print menus,
    touch files or manage other products.

    OCP: a new type of product is added by writing a new subclass, not by
    changing this class. Product cannot be instantiated directly because
    get_fulfilment_info() has no implementation here.
    """

    # Lab 8, sections 2.2 and 5: association and explicit design types.
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier) -> None:
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if stock < 0:
            raise ValueError("Stock cannot be negative.")
        # Double underscore marks these as private: outside code should
        # use the public methods below instead of changing them directly.
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.supplier: Supplier = supplier

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def price(self) -> float:
        return self.__price

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        """Lab 8, section 6.3: set a nonnegative stock level for every subtype."""
        # The Product decides what counts as a valid stock level.
        if quantity < 0:
            raise ValueError("Stock cannot be negative.")
        self.__stock = int(quantity)

    def display_information(self) -> None:
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
        self.supplier.display_information()

    def to_dict(self) -> ProductRecord:
        # Subclasses extend this with their type and additional attributes.
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict(),
        }

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return a message explaining how this product reaches the customer."""
