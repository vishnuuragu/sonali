import frappe
from datetime import datetime

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
    fields = frappe.db.get_value("Bulk Coupon", {"uuid": custom_uuid}, ["name", "coupon_price", "isredeem", "serial_number","date_of_redeem"], as_dict=True)
    if not fields:
        frappe.response.update({
            "status": 404,
            "message": f"UUID Not Found: {custom_uuid}"
        })
        return

    # Fetch the Item Code linked to the Serial No
    serial_number = fields.serial_number
    if not serial_number:
        frappe.response.update({
            "status": 404,
            "message": f"No product is linked for Serial No: {serial_number}"
        })
        return

    # Fetch additional details about the item
    coupon_price = fields.coupon_price
    

    if not coupon_price :
        frappe.response.update({
            "status": 404,
            "message": f"Details not found for custom UUID: {custom_uuid}"
        })
        return

    # Set the response directly
    frappe.response.update({
        "status": 200,
        "custom_uuid": custom_uuid,
        "serial_no": serial_number,
        "coupon_price": coupon_price,
        "is_redeem": fields.isredeem,
        "date_of_redeem": fields.date_of_redeem
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
    if not custom_uuid or custom_redeem is None:
        frappe.response.update({
            "status": 400,
            "message": "Both 'custom_uuid' and 'custom_redeem' are required."
        })
        return

    # Fetch the Bulk Coupon linked to custom_uuid
    bulk_coupon = frappe.db.get_value("Bulk Coupon", {"uuid": custom_uuid}, ["name", "isredeem"], as_dict=True)
    if not bulk_coupon:
        frappe.response.update({
            "status": 404,
            "message": f"UUID Not Found: {custom_uuid}"
        })
        return
    
    # Check current redeem status
    current_redeem_status = bulk_coupon.isredeem
    if current_redeem_status == 1 and int(custom_redeem) == 1:
        frappe.response.update({
            "status": 400,
            "message": f"Bulk Coupon {bulk_coupon.name} is already marked as redeemed."
        })
        return
    if current_redeem_status == 1 and int(custom_redeem) == 0:
        frappe.response.update({
            "status": 400,
            "message": f"Bulk Coupon {bulk_coupon.name} is already marked as redeemed and value can't be changed."
        })
        return
    if current_redeem_status == 0 and int(custom_redeem) == 0:
        frappe.response.update({
            "status": 400,
            "message": f"Bulk Coupon {bulk_coupon.name} already has the same value."
        })
        return

    # Update the redeem status and date_of_redeem in Bulk Coupon
    bulk_coupon_doc = frappe.get_doc("Bulk Coupon", bulk_coupon.name)
    bulk_coupon_doc.isredeem = custom_redeem
    if int(custom_redeem) == 1:  # Only set date_of_redeem when redeeming
        bulk_coupon_doc.date_of_redeem = datetime.now()
    else:
        bulk_coupon_doc.date_of_redeem = None  # Clear the date if unredeeming
    bulk_coupon_doc.save(ignore_permissions=True)  # Save changes, ignoring permissions if needed

    # Set the response directly
    frappe.response.update({
        "status": 200,
        "message": f"Bulk Coupon {bulk_coupon.name} updated successfully.",
        "custom_uuid": custom_uuid,
        "is_redeem": custom_redeem,
        "date_of_redeem": bulk_coupon_doc.date_of_redeem
    })
