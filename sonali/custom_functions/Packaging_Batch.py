import frappe

@frappe.whitelist()
def update_serial_weight(doc, method):
    """
    This function loops through the child table rows (serial_nos) of a Packaging Batch document.
    For each row, if a serial_no and a weight are provided, it updates the 'custom_weight' field 
    on the corresponding Serial No record.
    """
    for row in doc.get("serial_nos") or []:
        if row.serial_no and row.weight is not None:
            frappe.db.set_value("Serial No", row.serial_no, "custom_weight", row.weight)
