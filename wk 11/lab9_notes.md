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
