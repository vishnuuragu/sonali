import frappe
import uuid
import qrcode
from frappe.utils import get_site_path

@frappe.whitelist()
def create_bulk_data(number_of_coupons, coupon_amount):
    """Server-side method to create bulk data for the custom doctype"""
    try:
        number_of_coupons = int(number_of_coupons)  # Ensure it's an integer
        for i in range(number_of_coupons):
            doc = frappe.new_doc("Bulk Coupon")
            doc.coupon_price = coupon_amount  # Replace 'additional_field' with your actual fieldname
            uuid_v4 = uuid.uuid4()
            doc.uuid = str(uuid_v4)
            qr_data = doc.uuid;  # Generate QR code data
            qr_image = qrcode.make(qr_data)
            qr_code_path = get_site_path("public", "files", f"{doc.uuid}.png")
            qr_image.save(qr_code_path)
            print(f"Generating QR code for Serial No: {doc.uuid}")
            doc.qr_image = f"/files/{doc.uuid}.png"
            print(doc.qr_image)
            doc.insert()

        return f"{number_of_coupons} records created successfully!"
    except Exception as e:
        frappe.throw(f"An error occurred while creating bulk data: {str(e)}")