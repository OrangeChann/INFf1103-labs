# INF1103 Week 11 — Lab 9

Lab title: **Design Patterns and Error Handling (Strategy, Factory,
Validation, Try / Except and Automated Tests)**.

This folder extends the Lab 8 system from `wk 10`; earlier weeks are untouched.
Labels below follow the lab's section numbers. Written answers in
`lab9_notes.md` / the Word document are AI-assisted drafts: review and put
them in your own words before submission.

## Files

| File | Lab section | Purpose |
| --- | --- | --- |
| `discount_strategy.py` | 2.2 | `DiscountStrategy` (abstract), `NoDiscount`, `PercentageDiscount`, `BulkDiscount` |
| `student_discount.py` | 2.4 | Fourth strategy (5%), added without changing `Order` |
| `order.py` | 2.3 | Takes a strategy (default `NoDiscount()`), `set_discount()`, `calculate_total()` calls `apply()` |
| `product_factory.py` | 3.2 | `ProductFactory.create()` — the only place that picks a product class |
| `product.py`, `order_line.py` | 4 | Price > 0, stock >= 0, order quantity > 0, each in its owning class |
| `input_helpers.py` | 5.1 | `get_positive_float()` and whole-number helpers that ask again |
| `product_loader.py`, `products.csv` | 5.2 | `load_products()` with try / except / else / finally |
| `main.py` | 2, 3, 5 | Menu: order option 6 = Set Discount, main option 9 = Load Products from CSV |
| `lab9_demo.py` | 2–5 | Labelled evidence for every Predict First question |
| `tests/` | 7 | 99 automated tests (see below) |
| `uml_class_diagram.png` / `.svg` | 6 | Updated UML (new/changed classes in orange) |
| `lab9_notes.md`, `Lab9_Predict_First_and_Reflection.docx` | all | 1.5 diagnosis, every Predict First, sections 6–8 |
| `build_deliverables.py` | — | Regenerates the Word document and the SVG from source |

The rest (`product.py` subclasses, `supplier.py`, `inventory.py`,
`inventory_file.py`, `can_be_shipped.py`, `inventory.json`) is the Lab 8 system,
now creating products through the factory.

## Run it locally

From this folder:

```powershell
cd "C:\Users\Elizabeth\INF1103-Labs\wk 11"
python -B -m unittest -v      # 99 tests, OK
python -B lab9_demo.py        # Predict First evidence, sections 2-5
python main.py                # the menu program
```

`lab9_demo.py` section 5.2 really renames `products.csv` for a moment to show
the missing-file case, then puts it back in a `finally` block.

## 7. Tests (`tests/` folder)

| Test file | What it covers |
| --- | --- |
| `test_discounts.py` | Strategies, Order delegating to `apply()`, no if/elif in Order, `set_discount()`, shared strategy, discount menu |
| `test_factory.py` | Each type created, `ValueError` for unknown type, menu and JSON loader use the factory |
| `test_validation.py` | Price, stock and order-quantity rules for every product type (LSP) |
| `test_exceptions.py` | Input helpers re-ask, `load_products` (lab CSV, missing file, bad rows, duplicates), safe save, no catch-all `except` |
| `test_products.py`, `test_relationships.py` | Lab 7 and Lab 8 regression tests |

## 9. Git and Docker workflow — your steps

**Commit checkpoint: after reviewing the notes, Word document and UML.**
The assistant has not staged, committed or pushed anything.

```powershell
cd "C:\Users\Elizabeth\INF1103-Labs\wk 11"
git status
git add .
git commit -m "Lab 9 sections 6-8: UML, test review, reflection and Word notes"
git push origin main
git log --oneline -10
```

Docker (same volume-mount workflow as previous labs):

```powershell
docker build -t inf1103-lab9 .
docker images inf1103-lab9
docker run --rm -v "${PWD}:/app" inf1103-lab9 python -B -m unittest -v
docker run --rm -v "${PWD}:/app" inf1103-lab9 python -B lab9_demo.py
docker run --rm -it -v "${PWD}:/app" inf1103-lab9
```

Suggested things to show in the interactive run: option 8 → create an order,
add lines, option 6 Set Discount (e.g. 3 = Bulk), option 3 Display (subtotal,
discount, total); option 2 Add Product typing `abc` and `-5` for the price
(asked again); option 9 Load Products from CSV. With the saved `inventory.json`
P001, D001 and P003 already exist, so option 9 reports them as duplicates —
the "3 products loaded" result is shown by `lab9_demo.py` (empty inventory).
Option 7 in the order menu goes back; option 6 in the main menu saves and exits.

Screenshots (Win+Shift+S), saved in this folder:

| Suggested file name | What must be visible |
| --- | --- |
| `git_workflow.png` | `git status`, your commit, the successful push and `git log` |
| `dockerimg.png` | Docker build success and `docker images inf1103-lab9` |
| `dockerTest.png` | The Docker test command and `Ran 99 tests` / `OK` |
| `dockerDemo.png` | The Docker demo output (sections 2–5) |
| `workingDocker_WorkingAPP.png` | The interactive program working in Docker |

Then commit the screenshots and push again:

```powershell
git add .
git commit -m "Add Lab 9 Git and Docker workflow screenshots"
git push origin main
git log --oneline -10
```

## Submission checklist

- [x] Python source files, including the `tests` folder
- [x] Predict First notes (prediction, what happened, what changed) — Word document
- [x] Updated UML class diagram with Strategy and Factory classes
- [x] Docker build, tests and demo verified
- [ ] Review / personalise the AI-assisted written answers (especially 8.5 and 8.6)
- [ ] Your own commit and push
- [ ] Git and Docker screenshots, then commit and push them

To regenerate the Word document after editing `lab9_notes.md`:

```powershell
python -B build_deliverables.py
```

This also rebuilds `uml_class_diagram.svg`. To re-export the PNG from it:

```powershell
& "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=2140,2720 --screenshot="$PWD\uml_class_diagram.png" "file:///$($PWD -replace '\\','/')/uml_class_diagram.svg"
```
