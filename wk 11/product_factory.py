"""Lab 9, section 3.2: centralised product creation (Factory pattern).

The factory owns the decision about which concrete Product class to build.
The rest of the program asks the factory for a Product and never needs to
import PhysicalProduct, DigitalProduct or SubscriptionProduct itself.

Section 3.3: this if/elif still has to change when a new product type is
added, so the factory itself does not satisfy OCP. That is accepted here: it is
the single place to update, and a more flexible design (e.g. a registry that
types add themselves to) would be over-engineering for three product types.
"""
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from product import Product
from subscription_product import SubscriptionProduct
from supplier import Supplier


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, *,
               weight: float = 0.0, download_size: float = 0.0,
               duration_months: int = 1) -> Product:
        """Return a new Product of the requested type.

        Arguments adjusted to my Lab 7/8 constructors: each type has one extra
        detail, passed by keyword. The defaults let a source that has no extra
        detail (such as products.csv in section 5.2) still create a product.
        """
        if product_type == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity,
                                   weight, supplier)
        elif product_type == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity,
                                  download_size, supplier)
        elif product_type == "subscription":
            return SubscriptionProduct(product_id, name, price, stock_quantity,
                                       duration_months, supplier)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
