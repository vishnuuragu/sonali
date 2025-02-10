import frappe

def execute(filters=None):
    columns = [
        {"label": "Product Code", "fieldname": "product_code", "fieldtype": "Data", "width": 150},
        {"label": "Product Name", "fieldname": "product_name", "fieldtype": "Data", "width": 200},
        {"label": "Colour", "fieldname": "colour", "fieldtype": "Data", "width": 100},
        {"label": "Coils/Drums", "fieldname": "coils_drums", "fieldtype": "Int", "width": 120},
        {"label": "Length (Mtrs)", "fieldname": "length", "fieldtype": "Float", "width": 150},
        {"label": "Master Carton Coils/Drums", "fieldname": "mc_coils_drums", "fieldtype": "Int", "width": 150},
    ]

    data = []

    # Fetch Regular Item Stock
    items = frappe.db.sql("""
        SELECT 
            i.variant_of AS product_code,
            i.item_name AS product_name,
            COALESCE(iv.attribute_value, 'TOTAL') AS colour,
            COUNT(sn.name) AS coils_drums,
            SUM(COALESCE(sn.custom_length, 0)) AS length
        FROM `tabSerial No` sn
        JOIN `tabItem` i ON sn.item_code = i.name
        LEFT JOIN `tabItem Variant Attribute` iv 
            ON i.name = iv.parent AND iv.attribute = 'Colour'
        WHERE i.variant_of IS NOT NULL
        GROUP BY i.variant_of, iv.attribute_value
    """, as_dict=True)

    # Fetch Master Carton Stock
    master_cartons = frappe.db.sql("""
        SELECT 
            i.name AS mc_item,
            LEFT(i.name, LOCATE('_MB', i.name) - 1) AS mc_product_code, 
            RIGHT(i.name, LENGTH(i.name) - LOCATE('-', i.name)) AS mc_colour, 
            SUM(sn.custom_length) AS mc_length,
            COUNT(sn.name) AS mc_coils_drums
        FROM `tabSerial No` sn
        JOIN `tabItem` i ON sn.item_code = i.name
        WHERE i.name LIKE '%_MB-%'
        GROUP BY i.name
    """, as_dict=True)

    # Convert Master Cartons into a Dictionary for Fast Lookup
    mc_dict = {(mc["mc_product_code"], mc["mc_colour"]): mc for mc in master_cartons}

    # Merge Data
    for item in items:
        mc = mc_dict.get((item["product_code"], item["colour"]), {})
        data.append({
            "product_code": item["product_code"],
            "product_name": item["product_name"],
            "colour": item["colour"],
            "coils_drums": item["coils_drums"],
            "length": item["length"],
            "mc_length": mc.get("mc_length", 0),
            "mc_coils_drums": mc.get("mc_coils_drums", 0),
        })

    return columns, data
