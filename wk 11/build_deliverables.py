"""Generate Lab 9's Word notes and vector UML class diagram (no dependencies).

Run from any directory with: python -B build_deliverables.py
This builds documents only; it does not run the program, tests or Docker.
"""
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
NOTES = ROOT / "lab9_notes.md"
WORD_FILE = ROOT / "Lab9_Predict_First_and_Reflection.docx"
SVG_FILE = ROOT / "uml_class_diagram.svg"


def build_word_notes() -> None:
    namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    ET.register_namespace("w", namespace)
    document = ET.Element(f"{{{namespace}}}document")
    body = ET.SubElement(document, f"{{{namespace}}}body")
    # Join Markdown's wrapped prose into Word paragraphs. A blank line ends a
    # paragraph; a heading, list item or labelled line starts a new one.
    paragraphs: list[str] = []
    pending: list[str] = []
    starters = ("- ", "(1)", "(2)", "(3)", "Prediction", "Observed result",
                "Change if different", "Why ")

    def flush() -> None:
        if pending:
            paragraphs.append(" ".join(pending))
            pending.clear()

    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("#"):
            flush()
            paragraphs.append(line)
        else:
            if line.startswith(starters) or line[:2] in [f"{n}." for n in range(1, 10)]:
                flush()
            pending.append(line)
    flush()
    for line in paragraphs:
        paragraph = ET.SubElement(body, f"{{{namespace}}}p")
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            properties = ET.SubElement(paragraph, f"{{{namespace}}}pPr")
            ET.SubElement(properties, f"{{{namespace}}}pStyle", {
                f"{{{namespace}}}val": "Title" if level == 1 else f"Heading{level - 1}"
            })
            line = line.lstrip("# ")
        run = ET.SubElement(paragraph, f"{{{namespace}}}r")
        text = ET.SubElement(run, f"{{{namespace}}}t")
        text.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        text.text = line.replace("`", "")
    section = ET.SubElement(body, f"{{{namespace}}}sectPr")
    ET.SubElement(section, f"{{{namespace}}}pgSz", {
        f"{{{namespace}}}w": "11906", f"{{{namespace}}}h": "16838"
    })
    ET.SubElement(section, f"{{{namespace}}}pgMar", {
        f"{{{namespace}}}top": "1134", f"{{{namespace}}}bottom": "1134",
        f"{{{namespace}}}left": "1134", f"{{{namespace}}}right": "1134",
    })
    styles = '''<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
<w:sz w:val="22"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:after="100"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr>
<w:rPr><w:b/><w:color w:val="C55A11"/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="23"/></w:rPr></w:style>
</w:styles>'''
    with ZipFile(WORD_FILE, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>''')
        archive.writestr("_rels/.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>''')
        archive.writestr("word/_rels/document.xml.rels", '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>''')
        archive.writestr("word/document.xml",
                         ET.tostring(document, encoding="utf-8", xml_declaration=True))
        archive.writestr("word/styles.xml", styles)


def build_uml() -> None:
    width, height = 2140, 2720
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="{width}" height="{height}" fill="white"/>
<style>text{{font-family:Consolas,monospace;font-size:17px;fill:#162638}}
.title{{font-size:28px;font-weight:bold}}.name{{font-size:23px;font-weight:bold}}
.edge{{fill:none;stroke:#162638;stroke-width:2}}.class{{fill:#f8fbfe;stroke:#162638;stroke-width:2}}
.new{{fill:#fff6ec;stroke:#c55a11;stroke-width:2.5}}
.relation{{font-size:19px;font-weight:bold;paint-order:stroke;stroke:white;stroke-width:6px}}
.label{{paint-order:stroke;stroke:white;stroke-width:6px}}</style>
<defs><marker id="triangle" markerWidth="20" markerHeight="20" refX="17" refY="10" orient="auto" markerUnits="userSpaceOnUse">
<path d="M 1 1 L 17 10 L 1 19 Z" fill="white" stroke="#162638" stroke-width="2"/></marker>
<marker id="arrow" markerWidth="16" markerHeight="16" refX="14" refY="8" orient="auto" markerUnits="userSpaceOnUse">
<path d="M 1 1 L 14 8 L 1 15" fill="none" stroke="#162638" stroke-width="2"/></marker></defs>
<text x="25" y="38" class="title">INF1103 Week 11 / Lab 9 — class diagram with Strategy and Factory (section 6)</text>
<text x="25" y="68">Orange boxes are new or changed in Lab 9.</text>''']

    def text(x: int, y: int, value: str, css: str = "") -> None:
        # SVG collapses leading spaces, so keep continuation-line indents
        # with non-breaking spaces.
        indent = len(value) - len(value.lstrip(" "))
        value = " " * indent + value.lstrip(" ")
        parts.append(f'<text x="{x}" y="{y}" class="{css}">{escape(value)}</text>')

    def box(x: int, y: int, box_width: int, name: str, attributes: list[str],
            methods: list[str], new: bool = False) -> int:
        box_height = 54 + 25 * len(attributes) + 18 + 25 * len(methods) + 12
        css = "new" if new else "class"
        parts.append(f'<rect x="{x}" y="{y}" width="{box_width}" height="{box_height}" class="{css}"/>')
        text(x + 14, y + 32, name, "name")
        parts.append(f'<path d="M{x} {y+45} H{x+box_width}" class="edge"/>')
        for index, attribute in enumerate(attributes):
            text(x + 12, y + 69 + index * 25, attribute)
        divider = y + 54 + 25 * len(attributes)
        parts.append(f'<path d="M{x} {divider} H{x+box_width}" class="edge"/>')
        for index, method in enumerate(methods):
            text(x + 12, divider + 28 + index * 25, method)
        return y + box_height

    def edge(path: str, marker: str = "", dashed: bool = False) -> None:
        end = f' marker-end="url(#{marker})"' if marker else ''
        dash = ' stroke-dasharray="9 6"' if dashed else ''
        parts.append(f'<path d="{path}" class="edge"{end}{dash}/>')

    # ---- Top row: Supplier, Product, CanBeShipped --------------------------
    box(20, 100, 470, "Supplier", [
        "+ supplier_id: String", "+ name: String", "+ contact_email: String"
    ], ["+ Supplier(supplier_id: String, name: String,", "    contact_email: String)",
        "+ display_information(): Void", "+ to_dict(): Map<String, String>"])
    product_bottom = box(680, 100, 650, "«abstract» Product", [
        "- __product_id: String {read-only product_id}", "- __name: String",
        "- __price: Real {read-only price, > 0}", "- __stock: Integer {>= 0}",
        "+ supplier: Supplier"
    ], ["+ Product(product_id: String, name: String,",
        "    price: Real, stock: Integer, supplier: Supplier)",
        "+ get_product_id(): String", "+ get_name(): String", "+ get_price(): Real",
        "+ get_stock(): Integer", "+ update_stock(quantity: Integer): Void",
        "+ display_information(): Void", "+ to_dict(): ProductRecord",
        "+ get_fulfilment_info(): String {abstract}",
        "- __check_stock(quantity: Integer): Void {static}"], new=True)
    box(1480, 100, 560, "«interface» CanBeShipped", [], [
        "+ calculate_shipping_cost(): Real {abstract}"
    ])

    # ---- Factory (section 3): left of Product ------------------------------
    factory_y = 420
    box(20, factory_y, 520, "ProductFactory", [], [
        "+ create(product_type: String,",
        "    product_id: String, name: String,",
        "    price: Real, stock_quantity: Integer,",
        "    supplier: Supplier, weight: Real = 0,",
        "    download_size: Real = 0,",
        "    duration_months: Integer = 1): Product",
        "    {static}",
    ], new=True)
    # Dependency: dashed line, open arrow, «creates»; no stored reference.
    edge(f"M540 {factory_y + 110} H680", marker="arrow", dashed=True)
    text(550, factory_y + 98, "«creates»", "label")

    # ---- Product subclasses ------------------------------------------------
    box(20, 800, 570, "PhysicalProduct", ["- __weight: Real", "+ BASE_SHIPPING_COST: Real = 5.0",
        "+ SHIPPING_COST_PER_KG: Real = 2.0"], [
        "+ PhysicalProduct(common..., weight: Real,", "    supplier: Supplier)",
        "+ get_weight(): Real", "+ display_information(): Void",
        "+ get_fulfilment_info(): String", "+ calculate_shipping_cost(): Real",
        "+ to_dict(): ProductRecord"
    ])
    box(760, 800, 570, "DigitalProduct", ["- __download_size: Real"], [
        "+ DigitalProduct(common..., download_size: Real,", "    supplier: Supplier)",
        "+ get_download_size(): Real", "+ display_information(): Void",
        "+ get_fulfilment_info(): String", "+ to_dict(): ProductRecord"
    ])
    box(1470, 800, 570, "SubscriptionProduct", ["- __duration_months: Integer"], [
        "+ SubscriptionProduct(common...,", "    duration_months: Integer, supplier: Supplier)",
        "+ get_duration_months(): Integer", "+ display_information(): Void",
        "+ get_fulfilment_info(): String", "+ to_dict(): ProductRecord"
    ])

    # ---- Inventory, OrderLine, Order, InventoryFile ------------------------
    inv_bottom = box(20, 1290, 600, "Inventory", ["- __products: Product [0..*]",
                                                 "+ products: Product [0..*] {snapshot}"], [
        "+ Inventory()", "+ add_product(product: Product): Boolean",
        "+ remove_product(product_id: String): Boolean",
        "+ find_product(product_id: String): Product [0..1]",
        "+ search_product(product_id: String): Product [0..1]",
        "+ update_stock(product_id: String,", "    quantity: Integer): Boolean",
        "+ get_products(): Product [0..*] {snapshot}",
        "+ display_all_products(): Void", "+ display_all(): Void"
    ])
    line_bottom = box(1480, 1290, 560, "OrderLine", [
        "- __product: Product {read-only product}",
        "- __quantity: Integer {read-only quantity, > 0}"
    ], ["+ OrderLine(product: Product, quantity: Integer)",
        "+ calculate_subtotal(): Real"], new=True)
    order_bottom = box(760, 1600, 570, "Order", [
        "+ order_id: String", "- __order_lines: OrderLine [0..*]",
        "+ order_lines: OrderLine [0..*] {snapshot}",
        "- __cancelled: Boolean {read-only cancelled}",
        "- __discount: DiscountStrategy {read-only discount}",
    ], ["+ Order(order_id: String,",
        "    discount: DiscountStrategy = NoDiscount)",
        "+ set_discount(discount: DiscountStrategy): Void",
        "+ add_order_line(product: Product,", "    quantity: Integer): Void",
        "+ remove_order_line(index: Integer): Void",
        "+ calculate_subtotal(): Real", "+ calculate_total(): Real",
        "+ cancel(): Void", "+ display_information(): Void"], new=True)
    box(20, 1790, 600, "InventoryFile", ["- __file_path: String"], [
        "+ InventoryFile(file_path: String)", "+ load(inventory: Inventory): Void",
        "+ save(inventory: Inventory): Void", "- __create_product(record: ProductRecord,",
        "    suppliers: Map<String, Supplier>): Product"
    ], new=True)
    loader_bottom = box(1480, 1810, 600, "«utility» product_loader", [], [
        "+ load_products(path: String,", "    inventory: Inventory,",
        "    supplier: Supplier): Void",
    ], new=True)
    text(1480, loader_bottom + 28, "Module-level function (not a class).")
    text(1480, loader_bottom + 53, "Reads products.csv; creates each product")
    text(1480, loader_bottom + 78, "through ProductFactory.create().")

    # ---- Strategy (section 2) ----------------------------------------------
    strategy_y = 2180
    strategy_bottom = box(760, strategy_y, 570, "«abstract» DiscountStrategy", [], [
        "+ apply(total: Real): Real {abstract}"
    ], new=True)
    row_y = 2420
    box(20, row_y, 480, "NoDiscount", [], ["+ apply(total: Real): Real"], new=True)
    box(550, row_y, 500, "PercentageDiscount", ["- __percentage: Real {0 < p <= 100}"], [
        "+ PercentageDiscount(percentage: Real)", "+ apply(total: Real): Real"], new=True)
    box(1100, row_y, 500, "BulkDiscount", ["- __threshold: Real {>= 0}", "- __amount: Real {> 0}"], [
        "+ BulkDiscount(threshold: Real, amount: Real)", "+ apply(total: Real): Real"], new=True)
    box(1650, row_y, 470, "StudentDiscount", ["+ RATE: Integer = 5 {static}"], [
        "+ apply(total: Real): Real"], new=True)

    # Generalisation: solid line, hollow triangle at DiscountStrategy.
    edge(f"M260 {row_y} V{row_y - 50} H890 V{strategy_bottom}", marker="triangle")
    edge(f"M800 {row_y} V{row_y - 30} H990 V{strategy_bottom}", marker="triangle")
    edge(f"M1350 {row_y} V{row_y - 30} H1100 V{strategy_bottom}", marker="triangle")
    edge(f"M1885 {row_y} V{row_y - 50} H1200 V{strategy_bottom}", marker="triangle")

    # Association Order -> DiscountStrategy: solid line, open arrow (navigable).
    edge(f"M1045 {order_bottom} V{strategy_y}", marker="arrow")
    text(1060, order_bottom + 30, "0..*", "relation")
    text(1060, strategy_y - 12, "1", "relation")
    text(1100, order_bottom + 70, "uses (association)", "label")

    # ---- Lab 8 relationships (unchanged) -----------------------------------
    edge("M490 205 H680")
    text(510, 185, "1", "relation")
    text(598, 185, "0..*", "relation")
    text(508, 233, "supplies")

    edge(f"M305 800 V720 H890 V{product_bottom}", marker="triangle")
    edge(f"M1045 800 V{product_bottom}", marker="triangle")
    edge(f"M1755 800 V720 H1200 V{product_bottom}", marker="triangle")
    edge("M590 965 H660 V80 H1700 V100", marker="triangle", dashed=True)

    edge(f"M320 1260 V1220 H705 V{product_bottom}")
    parts.append('<path d="M320 1290 L309 1275 L320 1260 L331 1275 Z" fill="white" stroke="#162638" stroke-width="2"/>')
    text(338, 1265, "0..*", "relation")
    text(708, product_bottom + 30, "0..*", "relation")
    text(350, 1200, "aggregates (shared membership)")

    edge("M1760 1290 V1245 H2090 V470 H1330")
    text(1340, 455, "1", "relation")
    text(1770, 1280, "0..*", "relation")
    text(1810, 1233, "refers to")

    edge(f"M1360 1700 H1760 V{line_bottom}")
    parts.append('<path d="M1330 1700 L1345 1689 L1360 1700 L1345 1711 Z" fill="#162638" stroke="#162638" stroke-width="2"/>')
    text(1365, 1685, "1", "relation")
    text(1772, line_bottom + 28, "0..*", "relation")
    text(1490, 1682, "creates / owns")

    parts.append(f'<path d="M320 1790 V{inv_bottom}" class="edge" stroke-dasharray="9 6" marker-end="url(#arrow)"/>')
    text(335, 1768, "uses")

    # ---- Key -----------------------------------------------------------------
    for index, line in enumerate([
        "Key: + public, - private. Void = no result (Python None).",
        "common... = product_id: String, name: String, price: Real,",
        "    stock: Integer (constructor order).",
        "Hollow triangle, solid line = inherits; dashed = implements.",
        "Dashed open arrow «creates» = dependency: ProductFactory",
        "    builds Products but does not keep a reference to them.",
        "Order —> DiscountStrategy = association: each Order uses",
        "    exactly 1 strategy (NoDiscount by default); one strategy",
        "    object can be shared by 0..* Orders.",
    ]):
        text(760, 1280 + index * 30, line)
    text(25, height - 20, "Lab 9 §6: Strategy (DiscountStrategy family) and Factory "
                          "(ProductFactory «creates» Product) added to the Lab 8 diagram.")
    parts.append("</svg>")
    SVG_FILE.write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    build_word_notes()
    build_uml()
    print(f"Generated {WORD_FILE.name} and {SVG_FILE.name}")
