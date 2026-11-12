"""Generate Lab 8's editable Word notes and vector UML without dependencies.

This script generates documentation, not program/test results or screenshots.
Run from any directory with: python -B build_deliverables.py
"""
from html import escape
from pathlib import Path
from xml.etree import ElementTree as ET
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent


def build_word_notes() -> None:
    namespace = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
    ET.register_namespace("w", namespace)
    document = ET.Element(f"{{{namespace}}}document")
    body = ET.SubElement(document, f"{{{namespace}}}body")
    # Join Markdown's wrapped prose into proper Word paragraphs.
    paragraphs: list[str] = []
    pending: list[str] = []
    for line in (ROOT / "lab8_notes.md").read_text(encoding="utf-8").splitlines():
        if not line or line.startswith(("#", "- ")):
            if pending:
                paragraphs.append(" ".join(pending))
                pending.clear()
            if line:
                paragraphs.append(line)
        else:
            pending.append(line)
    if pending:
        paragraphs.append(" ".join(pending))
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
        text.text = line.replace("`", "")
    section = ET.SubElement(body, f"{{{namespace}}}sectPr")
    ET.SubElement(section, f"{{{namespace}}}pgSz", {
        f"{{{namespace}}}w": "11906", f"{{{namespace}}}h": "16838"
    })
    styles = '''<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
<w:sz w:val="22"/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/>
<w:rPr><w:b/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/>
<w:pPr><w:keepNext/><w:spacing w:before="240" w:after="120"/></w:pPr>
<w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/>
<w:pPr><w:keepNext/></w:pPr><w:rPr><w:b/><w:sz w:val="24"/></w:rPr></w:style>
</w:styles>'''
    with ZipFile(ROOT / "Lab8_Predict_First_and_Reflection.docx", "w", ZIP_DEFLATED) as archive:
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
        archive.writestr("word/document.xml", ET.tostring(document, encoding="utf-8", xml_declaration=True))
        archive.writestr("word/styles.xml", styles)


def build_uml() -> None:
    parts = ['''<svg xmlns="http://www.w3.org/2000/svg" width="2140" height="2070" viewBox="0 0 2140 2070">
<rect width="2140" height="2070" fill="white"/>
<style>text{font-family:Consolas,monospace;font-size:17px;fill:#162638}
.title{font-size:28px;font-weight:bold}.name{font-size:23px;font-weight:bold}
.edge{fill:none;stroke:#162638;stroke-width:2}.class{fill:#f8fbfe;stroke:#162638;stroke-width:2}
.relation{font-size:19px;font-weight:bold;paint-order:stroke;stroke:white;stroke-width:6px}</style>
<defs><marker id="triangle" markerWidth="20" markerHeight="20" refX="17" refY="10" orient="auto" markerUnits="userSpaceOnUse">
<path d="M 1 1 L 17 10 L 1 19 Z" fill="white" stroke="#162638" stroke-width="2"/></marker>
<marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto"><path d="M 1 1 L 10 6 L 1 11" fill="none" stroke="#162638"/></marker></defs>
<text x="25" y="38" class="title">INF1103 Week 10 / Lab 8 — typed class diagram (sections 5.3 and 8)</text>''']

    def text(x: int, y: int, value: str, css: str = "") -> None:
        parts.append(f'<text x="{x}" y="{y}" class="{css}">{escape(value)}</text>')

    def box(x: int, y: int, width: int, name: str,
            attributes: list[str], methods: list[str]) -> int:
        height = 54 + 25 * len(attributes) + 18 + 25 * len(methods) + 12
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" class="class"/>')
        text(x + 14, y + 32, name, "name")
        parts.append(f'<path d="M{x} {y+45} H{x+width}" class="edge"/>')
        for index, attribute in enumerate(attributes):
            text(x + 12, y + 69 + index * 25, attribute)
        divider = y + 54 + 25 * len(attributes)
        parts.append(f'<path d="M{x} {divider} H{x+width}" class="edge"/>')
        for index, method in enumerate(methods):
            text(x + 12, divider + 28 + index * 25, method)
        return y + height

    def edge(path: str, triangle: bool = False, dashed: bool = False) -> None:
        marker = ' marker-end="url(#triangle)"' if triangle else ''
        dash = ' stroke-dasharray="8 6"' if dashed else ''
        parts.append(f'<path d="{path}" class="edge"{marker}{dash}/>')

    box(20, 100, 470, "Supplier", [
        "+ supplier_id: String", "+ name: String", "+ contact_email: String"
    ], ["+ Supplier(supplier_id: String, name: String,", "    contact_email: String)",
        "+ display_information(): Void", "+ to_dict(): Map<String, String>"])
    product_bottom = box(680, 100, 650, "«abstract» Product", [
        "- __product_id: String {read-only product_id}", "- __name: String",
        "- __price: Real {read-only price}", "- __stock: Integer", "+ supplier: Supplier"
    ], ["+ Product(product_id: String, name: String,", "    price: Real, stock: Integer, supplier: Supplier)",
        "+ get_product_id(): String", "+ get_name(): String", "+ get_price(): Real",
        "+ get_stock(): Integer", "+ update_stock(quantity: Integer): Void",
        "+ display_information(): Void", "+ to_dict(): ProductRecord",
        "+ get_fulfilment_info(): String {abstract}"])
    box(1480, 100, 560, "«interface» CanBeShipped", [], [
        "+ calculate_shipping_cost(): Real {abstract}"
    ])
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
    inv_bottom = box(20, 1290, 600, "Inventory", ["- __products: Product [0..*]", "+ products: Product [0..*] {snapshot}"], [
        "+ Inventory()", "+ add_product(product: Product): Boolean",
        "+ remove_product(product_id: String): Boolean",
        "+ find_product(product_id: String): Product [0..1]",
        "+ search_product(product_id: String): Product [0..1]",
        "+ update_stock(product_id: String,", "    quantity: Integer): Boolean",
        "+ get_products(): Product [0..*] {snapshot}",
        "+ display_all_products(): Void", "+ display_all(): Void"
    ])
    line_bottom = box(1480, 1290, 560, "OrderLine", [
        "- __product: Product {read-only product}", "- __quantity: Integer {read-only quantity}"
    ], ["+ OrderLine(product: Product, quantity: Integer)", "+ calculate_subtotal(): Real"])
    box(760, 1600, 570, "Order", [
        "+ order_id: String", "- __order_lines: OrderLine [0..*]",
        "+ order_lines: OrderLine [0..*] {snapshot}",
        "- __cancelled: Boolean {read-only cancelled}"
    ], ["+ Order(order_id: String)", "+ add_order_line(product: Product,",
        "    quantity: Integer): Void", "+ remove_order_line(index: Integer): Void",
        "+ calculate_total(): Real", "+ cancel(): Void", "+ display_information(): Void"])
    box(20, 1790, 600, "InventoryFile", ["- __file_path: String"], [
        "+ InventoryFile(file_path: String)", "+ load(inventory: Inventory): Void",
        "+ save(inventory: Inventory): Void", "- __create_product(record: ProductRecord,",
        "    suppliers: Map<String, Supplier>): Product"
    ])

    # Association: no diamonds on either reference-only relationship.
    edge("M490 205 H680")
    text(510, 185, "1", "relation")
    text(618, 185, "0..*", "relation")
    text(508, 233, "supplies")

    # Generalisation: solid line, hollow triangle at Product.
    edge(f"M305 800 V720 H890 V{product_bottom}", triangle=True)
    edge(f"M1045 800 V{product_bottom}", triangle=True)
    edge(f"M1755 800 V720 H1200 V{product_bottom}", triangle=True)
    # Interface realisation: dashed line, hollow triangle at the interface.
    edge("M590 965 H650 V65 H1700 V100", triangle=True, dashed=True)

    # Aggregation: hollow diamond at Inventory; shared products are permitted.
    edge(f"M320 1260 V1220 H705 V{product_bottom}")
    parts.append('<path d="M320 1290 L309 1275 L320 1260 L331 1275 Z" fill="white" stroke="#162638" stroke-width="2"/>')
    text(338, 1265, "0..*", "relation")
    text(708, product_bottom + 30, "0..*", "relation")
    text(350, 1200, "aggregates (shared membership)")

    edge("M1760 1290 V1245 H2090 V470 H1330")
    text(1340, 455, "1", "relation")
    text(1770, 1280, "0..*", "relation")
    text(1810, 1233, "refers to")

    # Composition: filled diamond at Order; a line has exactly one owner.
    edge(f"M1360 1700 H1760 V{line_bottom}")
    parts.append('<path d="M1330 1700 L1345 1689 L1360 1700 L1345 1711 Z" fill="#162638" stroke="#162638" stroke-width="2"/>')
    text(1365, 1685, "1", "relation")
    text(1772, line_bottom + 28, "0..*", "relation")
    text(1490, 1682, "creates / owns")

    parts.append(f'<path d="M320 1790 V{inv_bottom}" class="edge" stroke-dasharray="8 6" marker-end="url(#arrow)"/>')
    text(335, 1768, "uses")
    text(760, 1285, "Visibility: + public; - private. Void = Python None.")
    text(760, 1320, "common... = product_id: String, name: String,")
    text(760, 1345, "price: Real, stock: Integer (constructor order).")
    text(760, 1380, "ProductRecord = typed JSON record; subtype fields")
    text(760, 1405, "are optional. SupplierRecord = Map<String, String>.")
    text(760, 1440, "Snapshots contain the same referenced objects.")
    text(760, 1475, "OrderLine lifecycle belongs to one Order;")
    text(760, 1500, "the referenced Product remains independent.")
    text(760, 1535, "Supplier IDs and Order IDs identify domain records.")
    text(25, 2040, "Lab 8 §8 review: plain association for Supplier/Product and OrderLine/Product; shared aggregation for Inventory/Product.")
    parts.append("</svg>")
    (ROOT / "uml_class_diagram.svg").write_text("\n".join(parts), encoding="utf-8")


if __name__ == "__main__":
    build_word_notes()
    build_uml()
    print("Generated Lab8_Predict_First_and_Reflection.docx and uml_class_diagram.svg")
