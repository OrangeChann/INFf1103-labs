# INF1103 Week 10 / Lab 8 — notes

These are AI-assisted draft answers. Review them, especially the predictions
and personal reflection, before submitting them as your own work.
Predictions below were recorded before running the Lab 8 demonstrations.
The corresponding Word document is generated from this file.

## 1. Review object relationships

### 1.1 Association
Product knows its Supplier, but neither is a part owned by the other. Both
objects are created independently. A stored reference alone does not imply
aggregation or composition.

### 1.2 Aggregation
Inventory groups existing Product objects. Removing an inventory reference,
emptying an inventory or transferring a product does not destroy the product
while another reference exists. Products are never constructed by Inventory.

### 1.3 Composition
Order creates and manages OrderLine objects. Each line belongs to one Order;
there is no API to adopt or transfer an existing line. Removing a line or
cancelling the order removes its lines from that order. Python can still keep
an object alive through an external reference: composition describes business
ownership, not a promise of immediate memory destruction.

## 2.2 Predict first — deleting the supplier variable

Prediction: both products can still display their supplier after `del supplier`.
The statement removes that variable binding, but both Product objects retain
references to the same Supplier object. A supplier created without any product
also works independently.

Observed result: both products displayed `SUP1 | Music and Games |
sales@example.com` after the variable was deleted, and their Supplier
references still referred to the same object. An independent supplier also
displayed information without products.
Change if different: none; the prediction matched the Docker demonstration.

## 3.2 Predict first — removing a product from Inventory A

Prediction: the product still works after removal because a local variable
still references it. Adding it to Inventory B stores that same object, rather
than a copy. Inventory owns its collection, not the product lifecycle.

Observed result: the removed Guitar still displayed its information and
fulfilment message. Inventory A no longer found it; Inventory B held exactly
the original object. Emptying B left the local product reference usable.
Change if different: none; the prediction matched the Docker demonstration.

## 4.3 Predict first — sharing a product between two orders

Prediction: adding one existing Product once to each of two Orders creates two
distinct OrderLine objects and uses one shared Product object. Each Order
creates its own line; the lines' product references compare equal with `is`.
In the complete demonstration a second product is also added to the first
order, so that whole scenario contains three lines and two products.

Observed result: the two guitar lines were distinct objects and both referred
to the original Guitar. The complete scenario had three lines and two products.
The first order total was $780.00 and became $180.00 after removing its guitar
line. Cancelling the second order removed its lines while keeping Guitar usable.
Change if different: none; the prediction matched the Docker demonstration.

## 5. Type hints as software design

Supplier references use Supplier; product collections use list[Product]; order
line collections use list[OrderLine]. find_product returns Product | None.
Mutating methods with no result return None; Inventory's add/remove/update
methods return bool to preserve the previous menu's success/failure contract.
The UML uses String, Integer, Real, Boolean, Void and typed collections with
multiplicities. Python hints describe this design but do not enforce it at
runtime. No Any annotation is used to avoid making a design decision.

## 6.3 LSP — parent expectation

Product.update_stock(quantity) replaces stock with a nonnegative quantity and
rejects a negative quantity with ValueError. PhysicalProduct, DigitalProduct
and the retained SubscriptionProduct inherit exactly that implementation.
They accept the same valid stock levels and preserve the meaning of get_stock.
Here, digital stock represents available licences or entitlements.

## 6.3 Diagnose — proposed DigitalProduct override

Yes, raising NotImplementedError for every update_stock call violates LSP:
code using Product expects a valid nonnegative stock update to succeed.
For this system I would remove that override from DigitalProduct and inherit
the parent's licence-stock behaviour. If digital stock truly had no meaning
in another domain, I would move stock operations to a separate stock-bearing
abstraction and revise Inventory accordingly.

## 7.2 Predict first — polymorphic fulfilment output

Prediction for the named demo products:
- PhysicalProduct: `Guitar requires physical shipping.`
- DigitalProduct: `Game is delivered digitally.`

Observed result: the mixed inventory printed exactly both predicted fulfilment
messages. It also used the correct specialised displays: Guitar's 3.50 kg
weight and Game's 2048.00 MB download size.
Change if different: none; the prediction matched the Docker demonstration.

## 7.3 Connect polymorphism to LSP

show_product_details(product: Product) calls display_information and
get_fulfilment_info without checking the subclass. The same calls dispatch to
the physical or digital implementation, demonstrating polymorphism. LSP
supports this design because both subclasses honour Product's operations,
return types and stock contract, so the caller needs no special cases.

## 8. UML review and AI use

Accepted: Supplier—Product uses association, with one Supplier per Product and
zero or more Products per Supplier. Order—OrderLine uses composition with
exactly one Order per line. Inheritance triangles point at Product.

Changed during review: use 0..* at the Inventory end instead of copying the
lab's illustrative 0..1. Our Inventory API allows the same Product reference
in multiple inventories, so shared aggregation matches the actual code.
The transfer demonstration still removes the Product from A before adding
it to B. OrderLine—Product remains an association, not composition.

## 9. Testing and responsibility review

test_products.py retains Lab 7 regression coverage, updated for Supplier.
test_relationships.py checks the Lab 8 relationships, lifecycle ownership,
totals, identity, type hints, stock contract and polymorphic behaviour.
lab8_demo.py prints labelled evidence for sections 2, 3, 4, 6 and 7.
Product manages product state; Supplier provides supplier information;
Inventory manages references; Order manages lines; OrderLine calculates its
subtotal; InventoryFile handles persistence; main.py handles interaction.
Orders are demonstration/session data and are not saved to inventory.json.
Order totals use the current product price, as specified in section 4.1.

## 10. Reflection task — all optional questions

### 10.1 Prediction mismatch
All four draft predictions matched the execution, so no correction was needed.
The demonstrations confirmed that del removes a binding rather than every
reference, and that each Order creates a new line while sharing the Product
reference. I would change a prediction if I had confused removing a reference
with destroying an object; that assumption would contradict the identity tests.

### 10.2 Group project application (example to personalise)
For a food-waste project, a Recipe can be associated with independently
maintained Ingredient records. A Pantry can aggregate existing FoodItem
objects, which can be transferred to another pantry. A Recipe can compose its
RecipeStep records, which have meaning only within that recipe.

### 10.3 References without ownership
Yes. Product.supplier is a stored reference used to display supplier
information. The Supplier is neither a constituent part of a Product nor
created and lifecycle-managed by that Product.

### 10.4 Product removal versus line ownership
Inventory groups independently created products; removing a reference changes
membership. An OrderLine records a product/quantity choice for one particular
Order, which creates it and removes it through its own methods.

### 10.5 One Product collection
list[Product] lets the same inventory operations work for all current and
future product subclasses. Separate subtype collections duplicate logic and
make callers depend on concrete classes.

### 10.6 Type hints
Hints communicate the expected collaborators, collection elements, accepted
inputs and return values. Editors and type checkers can use them to detect
mistakes without changing Python's dynamic runtime behaviour.

### 10.7 Language independence
Yes. Classes, inheritance, associations, multiplicities and ownership still
make sense in Java or C#. The syntax for collections, optional results and
interfaces would change, while the design relationships remain the same.

### 10.8 Inheritance can violate LSP
Yes. DigitalProduct could inherit Product but reject every stock update.
It would still be a subclass syntactically, yet break callers that rely on
Product's promise to accept nonnegative stock quantities.

## 11. Git and Docker workflow

Follow README.md for commands and the screenshot checklist. No commits or
pushes are performed by the assistant. Capture Git evidence after making
your own commit so the screenshot shows the completed lab commit.

The local Python 3.14 run and Docker Python 3.11 run both passed all 48 tests.
The Docker demo completed every assertion. The Docker menu smoke test showed
a $2539.99 two-product order, $139.99 after removing the physical line, then
$0.00 after cancellation. The generated text logs have been removed in favour
of screenshots. Save your labelled Git and Docker screenshots in evidence/.
