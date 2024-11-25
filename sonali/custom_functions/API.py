import frappe

@frappe.whitelist(allow_guest=True)  # Makes the method accessible via API
def get_product_details_by_uuid(custom_uuid):
    # Fetch the Serial No linked to the custom_uuid
    serial_no = frappe.db.get_value("Serial No", {"custom_uuid": custom_uuid}, "name")
    if not serial_no:
        frappe.throw(f"No Serial No found for custom UUID: {custom_uuid}")

    # Fetch the Item Code linked to the Serial No
    item_code = frappe.db.get_value("Serial No", serial_no, "item_code")
    if not item_code:
        frappe.throw(f"No Item found for Serial No: {serial_no}")

    # Fetch additional details about the item
    item_details = frappe.db.get_value(
        "Item",
        item_code,
        # ["item_name", "description", "item_group", "brand", "stock_uom"],
        as_dict=True
    )

    # Include Serial No specific details
    serial_details = frappe.db.get_value(
        "Serial No",
        serial_no,
        # ["warehouse", "status", "warranty_expiry_date"],
        ["custom_redeem"],
        as_dict=True
    )

    if not item_details or not serial_details:
        frappe.throw(f"Details not found for custom UUID: {custom_uuid}")

    # Combine and return details
    return {
        "custom_uuid": custom_uuid,
        "serial_no": serial_no,
        "item_code": item_code,
        # **item_details,
        **serial_details
    }


@frappe.whitelist(allow_guest=True)  # Makes the method accessible via API
def update_status_by_uuid(custom_uuid, custom_redeem):
    # Validate inputs
    if not custom_uuid or not custom_redeem:
        frappe.throw("Both 'custom_uuid' and 'new_status' are required.")

    # Fetch the Serial No linked to custom_uuid
    serial_no = frappe.db.get_value("Serial No", {"custom_uuid": custom_uuid}, "name")
    if not serial_no:
        frappe.throw(f"No Serial No found for custom UUID: {custom_uuid}")

    # Update the status field in Serial No
    serial_doc = frappe.get_doc("Serial No", serial_no)
    serial_doc.custom_redeem = custom_redeem
    serial_doc.save(ignore_permissions=True)  # Save changes, ignoring permissions if needed

    # Return success response
    return {
        "message": f"Status updated successfully for Serial No: {serial_no}",
        "serial_no": serial_no,
        "custom_redeem": custom_redeem
    }
