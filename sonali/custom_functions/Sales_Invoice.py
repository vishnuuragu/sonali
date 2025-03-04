import frappe

@frappe.whitelist()
def get_serial_and_batch_details_from_sales_invoice(sales_invoice):
    sales_invoice_doc = frappe.get_doc("Sales Invoice", sales_invoice)
    serial_and_batch_details = []
    serial_nos = []
    
    for item in sales_invoice_doc.items:
        if item.delivery_note:
            delivery_note_doc = frappe.get_doc("Delivery Note", item.delivery_note)
            
            for dn_item in delivery_note_doc.items:
                if dn_item.serial_and_batch_bundle and dn_item.item_code == item.item_code:
                    serial_and_batch_details.append({
                        "delivery_note": item.delivery_note,
                        "item_code": dn_item.item_code,
                        "serial_and_batch_bundle": dn_item.serial_and_batch_bundle
                    })
                    
                    serial_and_batch_bundle = frappe.get_doc("Serial and Batch Bundle", dn_item.serial_and_batch_bundle)
                    for serial_no in serial_and_batch_bundle.entries:
                        serial_nos.append({
                            "serial_no": serial_no.serial_no,
                            "item_code": dn_item.item_code,
                            "weight": serial_no.custom_weight
                        })

    return serial_nos