"""Lab 9, section 5.2: load products from a CSV file without crashing.

try    - open the file; this is the only operation that can raise
         FileNotFoundError, so it is the only line inside this try.
except - the file is missing: print a simple message and stop loading.
else   - the file opened: read the rows. Each row has its own try / except
         ValueError, so one bad row is reported and skipped and the rest load.
finally - always runs, whether the file was found or not.
"""
import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            loaded = 0
            # Line 1 is the header, so the first product is on line 2.
            for line_number, row in enumerate(reader, start=2):
                if not row:
                    continue  # ignore blank lines
                try:
                    # A row with the wrong number of columns, a price that is
                    # not a number, an unknown type or a rule broken inside
                    # Product all raise ValueError.
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(
                        product_type, product_id, name, float(price),
                        int(stock_quantity), supplier)
                except ValueError as error:
                    print(f"Line {line_number} skipped ({','.join(row)}): {error}")
                    continue
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Line {line_number} skipped: product ID "
                          f"{product_id} already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
