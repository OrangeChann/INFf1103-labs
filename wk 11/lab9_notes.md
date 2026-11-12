# INF1103 Week 11 / Lab 9 — Predict First notes

These are AI-assisted draft answers. Review them and put them in your own
words before you submit. Each prediction was written down before the
matching code was run; the observed result was added afterwards.
The Word document is generated from this file.

## 1. Review design patterns and error handling

Question kept in mind throughout: what problem am I solving, and is this the
simplest design that solves it? A pattern is a design decision, not a rule.

- Design pattern: a reusable solution template for a recurring design problem.
  It is not finished code or a library.
- Strategy: each way of doing one task (here, a discount) becomes its own class
  behind a shared method, so a new option is a new class, not an edit.
- Factory: one place owns the decision about which concrete class to create,
  so the rest of the program only needs to know about Product.
- Validation: if-checks that reject bad data before it is used (raise ValueError).
- Exception handling: try / except around operations that can fail at run time
  (float("abc"), opening a missing file), caught specifically, with a simple
  message, and the user is asked again instead of continuing with bad data.

## 1.5 Diagnose — my Lab 8 code (week 10 folder)

(1) if/elif blocks that choose between different behaviours:
- main.py create_product(): if product_type == "1" / "2" / else picks which
  product class to build and which extra detail to ask for.
- inventory_file.py __create_product(): if product_type == "physical" /
  "digital" / "subscription" picks the class when loading JSON.
- main.py main() and manage_orders(): if/elif on the menu choice. These choose
  which menu action to run; they are user-interface dispatch, so I will leave
  them as they are (a pattern here would be over-engineering).
- There is no discount logic yet; section 2 must add it without an if/elif.

(2) Every place a PhysicalProduct or DigitalProduct is created directly:
- main.py create_product() lines 24 and 27 (and SubscriptionProduct, line 29).
- inventory_file.py __create_product() lines 73 and 75 (and Subscription, 77).
- The tests also build products directly. That is acceptable: a unit test of
  one class should construct that class. Application code will use the factory.
So the same "which class?" decision is repeated in two application files.

(3) Places where bad input or a missing file could cause a problem:
- main.py add_product(): price = float(input("Price: ")). Typing "abc" is
  caught, but the whole product is thrown away and the user must start again.
  A price of 0 is accepted, because Product only rejects price < 0.
- inventory_file.py save(): open(path, "w") has no try / except, so a
  read-only folder or locked file (OSError) would crash the program on exit.
- inventory_file.py load() checks os.path.exists() before opening instead of
  catching FileNotFoundError; section 5.2 uses the try / except style instead.

## 2.1 Predict first — adding a 5% student discount

Prediction (without Strategy): the Order class must change. Its
calculate_total() method would need a new elif discount_type == "student"
branch returning total * 0.95. Every new discount means editing and
re-testing that same method, which breaks the Open/Closed Principle.

Prediction (with my Strategy version): no existing class changes. I add one new
class, StudentDiscount(DiscountStrategy), with its own apply(). Order,
NoDiscount, PercentageDiscount and BulkDiscount stay exactly as they are.
Only the menu gains an option so a user can pick it; that is user-interface
wiring, not discount logic.

Observed result: adding StudentDiscount needed only the new file
student_discount.py. order.py was not edited; the demo's OCP check found no
"Percentage", "Bulk", "Student" or "elif" anywhere in the Order class. The menu
(main.py choose_discount) gained option 4 so a user can select it.
Change if different: none; the prediction matched.

## 2.3 Predict first — order lines adding up to 250

Prediction: with BulkDiscount(200, 20), 250 is at least 200, so
calculate_total() returns 250 - 20 = 230.00.
After set_discount(PercentageDiscount(10)) on the same order, the bulk
strategy is replaced, not stacked, and the lines have not changed, so it
returns 250 x 0.9 = 225.00 (10% of 250, not 10% of 230).

Observed result: subtotal 250.00; BulkDiscount(200, 20) gave 230.00; after
set_discount(PercentageDiscount(10)) the same order gave 225.00.
Change if different: none; the prediction matched. It confirmed that
set_discount() replaces the strategy rather than adding a second discount.

## 2.4 Predict first — Order and DiscountStrategy relationship

Prediction: association. A discount is something the order uses, not a part of
the order. The strategy object is created outside Order (or NoDiscount by
default) and passed in, it can be replaced with set_discount(), and two orders
can share the same PercentageDiscount object because strategies hold no
order-specific data. Deleting an order does not destroy the strategy.
Multiplicity: each Order uses exactly 1 DiscountStrategy (never none, because
NoDiscount is the default); each DiscountStrategy object is used by 0..* Orders.

Observed result: two orders were created with the same PercentageDiscount
object; first.discount is second.discount was True and each order got its own
correct total (90.00 and 270.00). After deleting both orders the strategy still
worked (apply(50) = 45.00), and an order created with no strategy used
"No discount". This matches association with 1 (strategy) to 0..* (orders).
Change if different: none; the prediction matched.

## 3.2 Predict first — ProductFactory.create("service", ...)

Prediction: "service" does not match "physical", "digital" or "subscription",
so the else branch runs and the line
raise ValueError(f"Unknown product type: {product_type}") inside
ProductFactory.create() raises ValueError: Unknown product type: service.
No product is returned. If nothing catches it, the exception travels back up
through every caller to the top of the program; Python prints a traceback
ending in that message and the program stops (exit code 1). Nothing after the
call runs. In section 5.2 the CSV loader catches this ValueError so one bad row
does not stop the whole load.

Observed result: run as its own program with nothing catching it, Python
printed a traceback pointing at product_factory.py line 41, the raise line in
create(), ending "ValueError: Unknown product type: service". The next line,
print('This line never runs'), did not run and the exit code was 1. When the
same call was wrapped in try / except ValueError, the message was printed and
the demo carried on.
Change if different: none; the prediction matched.

## 3.3 Predict first — adding a BundleProduct

Prediction, before the factory (Lab 8 code): 3 places in 2 files, plus the new
class itself.
1. main.py create_product(): a new branch, plus a new import.
2. inventory_file.py __create_product(): a new branch, plus a new import.
3. main.py add_product(): the menu text and the list of valid choices.
Places 1 and 2 both decide "which class to build", so the same decision is
duplicated.

Prediction, after the factory: 2 places, plus the new class itself.
1. product_factory.py create(): one new elif branch and import. This is the
   only place that decides which class to build.
2. main.py PRODUCT_MENU: one new line so a user can choose it (the menu has
   to offer the new option whatever the design).
inventory_file.py no longer changes, because it passes the record's extra
fields straight to the factory.

Why the factory still breaks OCP: create() is an if/elif on the type name, so
adding a type means modifying the factory, not only extending the program.
Why that is acceptable here: the change is in one small, obvious, tested
place instead of being repeated around the program. A design that avoids
editing the factory (for example a registry that each class adds itself to)
would add complexity this three-type system does not need — the simplest
design that solves the current problem.

Observed result: after the change, the demo's import check shows main.py and
inventory_file.py import none of PhysicalProduct, DigitalProduct or
SubscriptionProduct; only product_factory.py does. So a BundleProduct would
change product_factory.py (one branch) and the PRODUCT_MENU line in main.py,
compared with three places in two files before.
Change if different: none; the prediction matched. This only holds because
the loader passes the record's remaining fields (weight, download_size, ...)
to the factory instead of reading each type's field by name as the Lab 8
loader did; otherwise inventory_file.py would still need a change.

## 4. Validation — where each rule lives

- Product (product.py) owns price and stock: price must be greater than zero
  (Lab 8 only rejected negative prices, so a price of 0 slipped through) and
  stock quantity cannot be negative, both in the constructor and in
  update_stock().
- OrderLine (order_line.py) owns its quantity: it must be greater than zero.
- The extra details stay with their subclass (weight, download size,
  duration), and the discount strategies check their own settings.
Each check raises ValueError with a clear message, so callers (the menu, the
loaders) decide how to report it; the classes never print or ask for input.

## 4. Predict first — may DigitalProduct skip or change the stock rule?

Prediction: no. Code that holds a Product (Inventory.update_stock, the menu,
the loaders) relies on the promise that stock is never negative. If
DigitalProduct skipped the check, a DigitalProduct could reach a state a
Product never can, so it could not safely substitute for a Product: an LSP
violation (a weaker guarantee). Changing the rule to be stricter (for example
refusing stock of 0) would also break LSP, because a caller doing something
valid for any Product would get an unexpected error. So DigitalProduct must
keep the rule exactly. The rule is written once in Product and inherited, so
DigitalProduct gets it through super().__init__() and the inherited
update_stock() without repeating or overriding it. (Digital stock means
available licences in my system, so "not negative" still makes sense.)

Observed result: a DigitalProduct created with stock -1 and update_stock(-1)
on an existing one were both rejected with "Stock quantity cannot be
negative.", and the stock stayed at 100. update_stock(0) was accepted.
DigitalProduct does not override update_stock, so it uses Product's rule.
The same checks pass for PhysicalProduct and SubscriptionProduct in
tests/test_validation.py. Price 0 is now rejected ("Price must be greater than
zero."), which Lab 8 had allowed.
Change if different: none; the prediction matched.

## 5.1 Predict first — get_positive_float with abc, -5, 12.50

Prediction (the prompt "Price: " is shown before every entry):
- abc: float("abc") raises ValueError, so the except block prints
  "Please enter a valid number, e.g. 12.50" and the loop asks again.
- -5: float("-5") works, but the validation check value <= 0 is True, so it
  prints "Please enter a number greater than zero." and continue asks again.
- 12.50: float("12.50") works and passes the check, so nothing extra is
  printed and the function returns 12.5 (a float, so it is 12.5, not "12.50").

So "Price: " appears three times, followed by those two messages, and the
returned value is 12.5.

Observed result (lab9_demo.py, section 5.1):
- Price: abc -> Please enter a valid number, e.g. 12.50
- Price: -5 -> Please enter a number greater than zero.
- Price: 12.50 -> nothing else printed; returned value 12.5

Change if different: none; the prediction matched. I added one extra check to
the lab's helper: float() also accepts "nan" and "inf", and nan <= 0 is False,
so "nan" would have been returned as a valid price. The helper now treats
non-finite numbers as invalid and asks again.

## 5.2 Predict first — loading products.csv

Prediction with products.csv present (open succeeds, so except is skipped;
else and finally run):
- Line 2 physical P001 Desk Lamp: loads.
- Line 3 digital D001 Photo Editor: loads.
- Line 4 service S001: the factory raises "Unknown product type: service";
  the row's own except ValueError reports and skips it, and loading carries on.
- Line 5 physical P002 Office Chair, price "abc": float("abc") raises
  ValueError before the factory is called; reported and skipped.
- Line 6 physical P003 Monitor Stand: loads.

Messages in order: the line 4 message, the line 5 message, then
"3 products loaded.", then "Load attempt finished." (finally always runs last).

Prediction after renaming products.csv: open() raises FileNotFoundError, so
except runs and prints "Products file not found: products.csv". else does
NOT run, so no rows are read and no "products loaded" line is printed.
finally still runs and prints "Load attempt finished." The program does not
crash, and the inventory is unchanged.

Observed result with products.csv present:
- Line 4 skipped (service,S001,Installation,30.00,5): Unknown product type: service
- Line 5 skipped (physical,P002,Office Chair,abc,3): could not convert string to float: 'abc'
- 3 products loaded.
- Load attempt finished.

The inventory held P001, D001 and P003.

Observed result after renaming products.csv: only
"Products file not found: products.csv" (except) and
"Load attempt finished." (finally) were printed; else did not run, nothing
crashed and the inventory stayed empty. The demo renames the file back
afterwards inside its own finally block.

Change if different: none; the prediction matched. Note that the CSV has no
weight or download size column, so loaded products use the factory's
defaults (0.00 kg / 0.00 MB). In the menu (option 9) with my saved
inventory.json, P001, D001 and P003 are reported as duplicate IDs (those IDs
already exist), so 0 products load there; the "3 products loaded" result is
for an empty inventory, as in the lab question and lab9_demo.py.

## 6. Updated UML class diagram

uml_class_diagram.png (generated from uml_class_diagram.svg) is the Lab 8
diagram with the Lab 9 classes added; new or changed classes are orange.
- DiscountStrategy is shown as «abstract» with apply(total: Real): Real
  {abstract}. NoDiscount, PercentageDiscount, BulkDiscount and StudentDiscount
  inherit from it (solid line, hollow triangle).
- Order to DiscountStrategy is an association with an open arrow from Order
  (Order knows its strategy; the strategy does not know the order).
  Multiplicity 1 at the DiscountStrategy end (NoDiscount by default, so never
  none) and 0..* at the Order end (one strategy object can be shared).
- ProductFactory has a dashed open arrow to Product labelled «creates»: a
  dependency, because it builds products but never stores them.
- Validation rules are written as constraints, e.g. price {> 0},
  stock {>= 0}, quantity {> 0}, percentage {0 < p <= 100}.
- load_products is a function, not a class, so it is drawn as a «utility»
  box with a note that it creates products through the factory.
- Python-specific names are translated (Real, Integer, String, Void,
  {static}, {abstract}) so a developer who does not know Python can read it.

## 7. Testing and review

Run from the wk 11 folder: python -m unittest -v (99 tests, all passing).
The tests live in the tests folder: test_discounts.py, test_factory.py,
test_validation.py and test_exceptions.py are new for Lab 9;
test_products.py and test_relationships.py are the Lab 7 and Lab 8 regression
tests, kept so earlier behaviour is not broken by the new design.

Lab checklist and the test that confirms each item:
- Order totals go through a DiscountStrategy with no discount if/elif:
  test_order_delegates_to_strategy_apply, test_order_contains_no_discount_type_logic.
- A new strategy needs no change to Order: test_new_strategy_needs_no_change_to_order
  (a HalfPrice strategy invented inside the test), plus StudentDiscount in its own file.
- set_discount() changes the strategy of an existing order:
  test_bulk_then_percentage_predict_first, test_menu_sets_student_discount.
- Products are created through ProductFactory: test_menu_and_loader_do_not_import_concrete_classes,
  test_menu_add_product_goes_through_factory, test_json_loader_goes_through_factory,
  test_products_are_created_through_factory.
- Unknown product type raises a clear ValueError: test_unknown_type_raises_clear_value_error.
- Invalid prices, stock and order quantities are rejected: test_validation.py (all types).
- Invalid user input is handled and the user is asked again:
  test_predict_first_abc_then_minus_5_then_12_50, test_add_product_asks_again_for_bad_price_and_stock,
  test_update_stock_asks_again.
- A missing products file is handled: test_missing_file_runs_except_and_finally_only.
- Bad rows are reported and skipped, valid rows still load:
  test_lab_file_loads_three_and_reports_two_bad_rows_in_order.
- Each except catches a specific exception:
  test_no_bare_or_catch_all_except_in_application_code (scans every .py file).

Two older tests changed on purpose, and the reason is recorded in the code:
the order-menu test now uses 7 for Back (6 is Set Discount), and the Lab 7
"bad weight adds nothing" test now expects the user to be asked again, as
section 1.4 requires. One Lab 7 test (a saved physical record with no weight
must be skipped) failed after the factory was added; I kept the test and
fixed the loader instead.

## 8. Reflection task (optional)

### 8.1 Where would a pattern add needless complexity?
The main menu's if/elif on the option number. A Command pattern (one class
per menu option) would add nine classes to replace a short, readable block
that only ever chooses which function to call. The same goes for Supplier and
Inventory: they have one behaviour each, so there is nothing to make
interchangeable. Shipping cost has a single formula, so a ShippingStrategy
would be a pattern looking for a problem.

### 8.2 Is moving the OCP issue into the factory a good trade-off?
Yes, for this system. Before, the "which class?" decision was repeated in
main.py and inventory_file.py; now it is in one small, tested method, and the
rest of the code depends only on Product. New product types are rare here
(three in three labs), so editing one elif is cheap. If types were added
often, or by other teams as plug-ins, a registry would be worth its extra
complexity.

### 8.3 When would rejecting the whole file be better?
When the rows only make sense together, so a partial load leaves the system
wrong: for example a complete price list replacing the old one, or stock
transfers where one missing row breaks the totals. Also when the file itself
is the wrong format (wrong header or column count on every row), when most
rows fail, or when a person must fix and approve the file before anything is
imported. Then the safer design is validate everything first, and load
nothing unless every row is valid.

### 8.4 Validation failure versus exception
A validation failure is my own rule saying the data is not acceptable, checked
with an if: Product(..., price=0, ...) fails "if price <= 0" and I raise
ValueError("Price must be greater than zero."). An exception (in the sense of
section 1.4) is an operation failing while it runs: float("abc") raises
ValueError, and open("products.csv") raises FileNotFoundError when the file
was renamed. They work together: the validation failure is reported by
raising an exception, and the caller (the menu or load_products) handles both
kinds in a specific except.

### 8.5 Which predictions did not match? (draft — replace with your own)
All the recorded Predict First answers matched the program output. While
building the lab, three assumptions turned out wrong and were changed:
- I assumed the factory's default weight would only affect the CSV. A Lab 7
  test showed a corrupt JSON record with no weight was now loaded instead of
  skipped, so the JSON loader now rejects records missing their type's fields.
- I assumed float() only returns ordinary numbers. It accepts "nan", and
  nan <= 0 is False, so get_positive_float would have returned nan as a price.
  I added a finite-number check.
- I expected menu option 9 to show "3 products loaded" too, but my saved
  inventory already had P001, D001 and P003, so all three were duplicates and
  0 loaded. The loader was right; my assumption about the data was wrong.

### 8.6 Group project — Strategy or Factory? (example to personalise)
For a food-waste project: Strategy would help for how expiry alerts are
chosen (e.g. alert 3 days before, alert by food category, no alerts), because
users switch between rules and new rules are likely. Factory would help if
food items come from several sources (barcode scan, manual entry, receipt
import) that must create FridgeItem, PantryItem or FrozenItem objects. It would
be over-engineering for screens or reports that only ever have one version;
there a plain function or class is simpler.

## 9. Git and Docker workflow

See README.md for the exact commands and the screenshot list. Commits and
pushes are made by me; the screenshots show my own Git and Docker output.
