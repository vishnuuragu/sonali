import frappe

@frappe.whitelist(allow_guest=True)
def get_product_details_by_uuid(custom_uuid):
    STATIC_TOKEN = frappe.get_conf().get("static_api_token")
    auth_header = frappe.get_request_header("X-Static-Token")
    if auth_header != STATIC_TOKEN:
        frappe.response.update({
            "status": 401,
            "message": "Unauthorized"
        })
        return

    # Fetch the Serial No linked to the custom_uuid
    serial_no = frappe.db.get_value("Serial No", {"custom_uuid": custom_uuid}, "name")
    if not serial_no:
        frappe.response.update({
            "status": 404,
            "message": f"UUID Not Found: {custom_uuid}"
        })
        return

    # Fetch the Item Code linked to the Serial No
    item_code = frappe.db.get_value("Serial No", serial_no, "item_code")
    if not item_code:
        frappe.response.update({
            "status": 404,
            "message": f"No Item found for Serial No: {serial_no}"
        })
        return

    # Fetch additional details about the item
    item_details = frappe.db.get_value(
        "Item",
        item_code,
        as_dict=True
    )

    # Include Serial No specific details
    serial_details = frappe.db.get_value(
        "Serial No",
        serial_no,
        ["custom_redeem"],
        as_dict=True
    )

    if not item_details or not serial_details:
        frappe.response.update({
            "status": 404,
            "message": f"Details not found for custom UUID: {custom_uuid}"
        })
        return

    # Set the response directly
    frappe.response.update({
        "status": 200,
        "custom_uuid": custom_uuid,
        "serial_no": serial_no,
        "item_code": item_code,
        **serial_details
    })


@frappe.whitelist(allow_guest=True)  # Makes the method accessible via API
def update_status_by_uuid(custom_uuid, custom_redeem):
    STATIC_TOKEN = frappe.get_conf().get("static_api_token")
    auth_header = frappe.get_request_header("X-Static-Token")
    if auth_header != STATIC_TOKEN:
        frappe.response.update({
            "status": 401,
            "message": "Unauthorized"
        })
        return

    # Validate inputs
    if not custom_uuid or not custom_redeem:
        frappe.response.update({
            "status": 400,
            "message": "Both 'custom_uuid' and 'custom_redeem' are required."
        })
        return

    # Fetch the Serial No linked to custom_uuid
    serial_no = frappe.db.get_value("Serial No", {"custom_uuid": custom_uuid}, "name")
    if not serial_no:
        frappe.response.update({
            "status": 404,
            "message": f"UUID Not Found: {custom_uuid}"
        })
        return
    
    # Fetch the current value of custom_redeem for the Serial No
    current_redeem_status = frappe.db.get_value("Serial No", serial_no, "custom_redeem")
    if current_redeem_status == 1 and int(custom_redeem) == 1:
        frappe.response.update({
            "status": 400,
            "message": f"Serial No {serial_no} is already marked as redeemed."
        })
        return

    # Update the status field in Serial No
    serial_doc = frappe.get_doc("Serial No", serial_no)
    serial_doc.custom_redeem = custom_redeem
    serial_doc.save(ignore_permissions=True)  # Save changes, ignoring permissions if needed

    # Set the response directly
    # Set the response directly
    frappe.response.update({
        "status": 200,
        "message": f"Serial No {serial_no} updated successfully.",
        "serial_no": serial_no,
        "custom_redeem": custom_redeem
    })
