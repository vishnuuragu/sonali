import frappe
import uuid

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
            doc.insert()

        return f"{number_of_coupons} records created successfully!"
    except Exception as e:
        frappe.throw(f"An error occurred while creating bulk data: {str(e)}")
