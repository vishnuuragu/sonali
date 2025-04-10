import frappe

@frappe.whitelist()
def get_delivery_note_weights(sales_invoice):
    # ✅ Ensure the Sales Invoice exists
    if not frappe.db.exists("Sales Invoice", sales_invoice):
        return {"error": f"Sales Invoice {sales_invoice} not found"}

    sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice)

    # ✅ Prevent modification of Submitted Sales Invoice
    if sales_invoice_doc.docstatus != 0:
        return {"error": "Cannot update a submitted Sales Invoice"}

    # ✅ Get linked Delivery Notes
    delivery_notes = list(set(item.delivery_note for item in sales_invoice_doc.items if item.delivery_note))
    if not delivery_notes:
        return {"error": "No Delivery Notes linked"}

    # ✅ Fetch weight and quantity data from Delivery Note Items
    dn_items = frappe.get_all(
        "Delivery Note Item",
        filters={"parent": ["in", delivery_notes]},
        fields=["item_code", "qty", "custom_weight", "custom_length", "parent as delivery_note"]
    )

    # ✅ Group items by Delivery Note + Item Code
    grouped_items = {}
    for dn_item in dn_items:
        key = (dn_item["delivery_note"], dn_item["item_code"])
        qty = float(dn_item.get("qty") or 0)
        weight = float(dn_item.get("custom_weight") or 0)
        length = float(dn_item.get("custom_length") or 0)

        if key in grouped_items:
            grouped_items[key]["qty"] += qty
            grouped_items[key]["total_weight"] += weight
            grouped_items[key]["total_length"] += length
        else:
            grouped_items[key] = {
                "delivery_note": dn_item["delivery_note"],
                "item_code": dn_item["item_code"],
                "qty": qty,
                "total_weight": weight,
                "total_length": length
            }

    updated_items = []
    sales_invoice_doc.items = []  # ✅ Clear existing items to avoid duplicates

    for key, grouped_item in grouped_items.items():
        new_item = sales_invoice_doc.append("items", {})
        new_item.item_code = grouped_item["item_code"]
        new_item.custom_weight_in_kg = round(grouped_item["total_weight"], 3)
        new_item.custom_length_in_m = round(grouped_item["total_length"], 3)
        new_item.qty = grouped_item["qty"]
        new_item.delivery_note = grouped_item["delivery_note"]
        new_item.rate = 0  # User will enter manually

        updated_items.append({
            "delivery_note": grouped_item["delivery_note"],
            "item_code": grouped_item["item_code"],
            "custom_weight_in_kg": new_item.custom_weight_in_kg,
            "custom_length_in_m": new_item.custom_length_in_m,
            "qty": grouped_item["qty"],
            "rate": 0
        })

    return {"updated_items": updated_items}
