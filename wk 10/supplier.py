"""Lab 8, section 2.1: a supplier exists independently of its products."""
from typing import TypedDict


class SupplierRecord(TypedDict):
    supplier_id: str
    name: str
    contact_email: str


class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(f"Supplier: {self.supplier_id} | {self.name} | {self.contact_email}")

    def to_dict(self) -> SupplierRecord:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }
