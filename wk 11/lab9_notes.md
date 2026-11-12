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
