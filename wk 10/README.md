# INF1103 Week 10 — Lab 8

Lab title: **Object-Oriented Relationships Part 2 (Association, Aggregation,
Composition, Type Hints and Liskov Substitution)**.

This folder extends the Lab 7 system from `wk 9`; earlier weeks are untouched.
Labels below follow the lab's section numbers. Written answers are AI-assisted
drafts: review and personalise them before submission.

## 1. Review object relationships

See sections 1.1–1.3 of `lab8_notes.md` or the Word document for association,
aggregation, composition and Python lifecycle explanations.

## 2. Association: Supplier and Product

- `supplier.py` (2.1): supplier ID, name, email and display method.
- `product.py` (2.2): required `supplier: Supplier` object reference.
- All three product subclasses forward the Supplier to `super()`.
- `lab8_demo.py`, label 2.2: creates products with one supplier, deletes the
  supplier variable, then displays supplier information through both products.
- Menu option 2 prompts for supplier details. An existing supplier ID reuses
  that supplier object. Supplier information is also saved to JSON.

Supplier IDs identify suppliers in this system; do not give different supplier
details the same ID. Old Lab 7 records without supplier data load with an
explicit `LEGACY` placeholder, whose details should be replaced with real data.

## 3. Aggregation: Inventory and Product

`inventory.py` stores a private `list[Product]`. `products` and `get_products()`
return collection copies containing the original Product references.
`add_product`, `remove_product`, and `find_product` manage membership; `find_product`
returns `Product | None`. Add/remove return `bool` to report success and preserve
the previous duplicate-ID behaviour. Menu option 7 removes a product.

Demo label 3.2 creates a product before its inventories, transfers it from A to
B, checks identity, and empties B while retaining a working product reference.
The API permits shared inventory membership; the UML uses `0..*` at both ends
of the aggregation to reflect that choice.

## 4. Composition: Order and OrderLine

`Order.add_order_line(product, quantity)` creates a new OrderLine internally.
`OrderLine.calculate_subtotal()` uses the current product price times quantity.
`Order.calculate_total()` delegates to its lines. Orders offer removal and
cancellation, and callers cannot transfer lines by modifying a returned list.

Menu option 8 opens order management: create, add line, display, remove line,
cancel or return. Quantities must be positive. Orders are kept for the current
session only; the lab does not require order file persistence or stock deduction.

Demo label 4.3 shows two products in one order, the same product in another
order, separate line identities, subtotals, totals, removal and cancellation.
The first order totals `$780.00`; after removing its guitar line it totals
`$180.00`. Cancelling the other order leaves the Product usable.

## 5. Type hints as software design

All domain constructors and methods declare parameter and result types.
Attributes and object collections use domain types; optional lookup uses
`Product | None`. No `Any` annotations are used. The JSON boundary uses
`ProductRecord` and `SupplierRecord` typed dictionaries, including optional
fields for subtype-specific values and legacy records.

`uml_class_diagram.svg` is the editable, scalable diagram;
`uml_class_diagram.png` is the submission image. `build_deliverables.py` contains
its source and generates both the SVG and Word notes. Its Python type checks
are not a substitute for a static type checker; the lab does not require one.

## 6. Liskov Substitution Principle

`show_product_details(product: Product)` in `lab8_demo.py` works unchanged for
PhysicalProduct and DigitalProduct. Each inherits the same nonnegative stock
contract, with digital stock representing licences. The notes include the
required parent expectation and 2–3 sentence diagnosis of the proposed broken
DigitalProduct override.

## 7. Polymorphism

The demo's section 7.2 uses one mixed `list[Product]` and one loop to call both
display and fulfilment methods. Inventory's display does the same. There are
no subtype checks to select these behaviours. The retained Lab 7 menu checks
the separate CanBeShipped interface only to offer its additional shipping cost;
JSON deserialisation selects a class from a stored type tag.

## 8. UML class diagram

The diagram includes Product (abstract), PhysicalProduct, DigitalProduct,
SubscriptionProduct, CanBeShipped, Supplier, Inventory, InventoryFile, Order
and OrderLine. It shows typed attributes, parameters/results, multiplicities,
plain associations, hollow aggregation diamond, filled composition diamond,
and generalisation triangles pointing to Product. The interface uses dashed
realisation. Notes section 8 records one accepted and one changed AI design
choice and explains the shared aggregation multiplicity.

## 9. Testing and review

Open PowerShell in this folder:

```powershell
cd 'C:\Users\Elizabeth\INF1103-Labs\wk 10'
& 'C:\Users\Elizabeth\AppData\Local\Programs\Python\Python314\python.exe' -B -m unittest -v
```

There are 48 tests: 26 retained Lab 7 regressions plus 22 Lab 8 tests.
`test_relationships.py` groups them by lab section and checks identity,
ownership, totals, type hints, LSP, polymorphism and menu/JSON integration.

Repeat the Docker commands in section 11 and capture their output as
screenshots in `evidence/`. The generated text logs have been removed;
screenshots will provide the Git and Docker workflow evidence.

## 10. Reflection task (optional, completed)

All eight reflection prompts have draft answers in `lab8_notes.md` and
`Lab8_Predict_First_and_Reflection.docx`. Personalise the group-project example
and review the predictions. All four predictions matched the demonstrated
results; the notes explain why.

## 11. Git and Docker workflow — YOUR final steps

**Commit checkpoint 1: after reviewing the Word answers and UML, commit the
implementation and documents.** The assistant has
not staged, committed or pushed anything.

From `wk 10`, review the working tree and stage this lab folder:

```powershell
git status
git add .
git diff --cached --stat
git commit -m "Complete Lab 8 relationships, type hints, LSP and polymorphism"
git push origin main
git log -10 --oneline
```

Run the lab's established Docker volume-mount workflow in this same folder:

```powershell
docker build -t inf1103-lab8 .
docker images inf1103-lab8
docker run --rm -v "${PWD}:/app" inf1103-lab8 python -B -m unittest -v
docker run --rm -v "${PWD}:/app" inf1103-lab8 python -B lab8_demo.py
docker run --rm -it -v "${PWD}:/app" inf1103-lab8
```

In the interactive program, use option 1 to display the mixed inventory, then
option 8 to create an order and add a physical and a digital product. Display
the order, remove a line, and cancel it. Option 6 in the order menu returns to
the main menu; option 6 there saves inventory and exits. This interactive
volume-mounted run saves intentional inventory edits back to your JSON file.

Take **actual screenshots** with Win+Shift+S. Save them using these section labels:

| Screenshot filename in `evidence/` | What must be visible |
| --- | --- |
| `11_Git_workflow.png` | Your `git status`, meaningful commit, successful push and `git log` output (use multiple images with `_1`, `_2` suffixes if necessary). |
| `11_Docker_build.png` | Docker build success and `docker images inf1103-lab8`. |
| `11_Docker_tests.png` | Docker test command and `Ran 48 tests` / `OK`. |
| `11_Docker_program.png` | Docker run command and working mixed inventory or order total (use extra screenshots if needed). |

Capture Git screenshots after your own commit. The screenshots are the
remaining workflow evidence to add before submission.

**Commit checkpoint 2: after saving your screenshots, commit the
submission evidence, then push again.**

```powershell
git status
git add .
git commit -m "Add Lab 8 Git and Docker workflow screenshots"
git push origin main
git log -10 --oneline
```

## Submission requirements — checklist

- [x] Updated Python source, including all Lab 7 classes.
- [x] Four numbered Predict First answers: predictions, observations, differences.
- [x] Word document containing notes, LSP diagnosis and optional reflection.
- [x] UML source SVG and PNG with typed relationships and multiplicities.
- [x] Type hints in implementation and matching UML design.
- [x] Test code demonstrating relationships, LSP and polymorphism.
- [x] Docker build, tests and program execution verified successfully.
- [ ] Review/personalise the AI-assisted written answers.
- [ ] Make your own meaningful commit and push.
- [ ] Capture and save the labelled Git and Docker screenshots.
- [ ] Commit/push the final screenshot evidence.

To regenerate the Word document after editing `lab8_notes.md`:

```powershell
& 'C:\Users\Elizabeth\AppData\Local\Programs\Python\Python314\python.exe' -B build_deliverables.py
```

This also rebuilds the SVG. If you change diagram source, re-export its PNG
from the SVG before submission. Week 10/Lab 8 is the folder/lab naming used
throughout; the unspaced `wk10` directory is unused.
