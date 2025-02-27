# Copyright (c) 2025, Vishnu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HWPACKING(Document):
	pass


@frappe.whitelist()
def fetch_stock_entries(work_order):
    if not work_order:
        return []

    # Fetch all Stock Entries related to this Work Order
    stock_entries = frappe.get_all("Stock Entry", 
                                   filters={"work_order": work_order, "stock_entry_type": "Manufacture"}, 
                                   fields=["name"])

    if not stock_entries:
        return []

    stock_entry_names = [entry["name"] for entry in stock_entries]

    # Fetch Serial and Batch Bundle records linked to the Stock Entries
    batch_records = frappe.get_all("Serial and Batch Bundle",
                                   filters={"voucher_no": ["in", stock_entry_names]},
                                   fields=["name", "batch_no", "item_code", "quantity"])

    # Fetch serial numbers for each Serial and Batch Bundle record
    for batch in batch_records:
        serial_nos = frappe.get_all("Serial and Batch Bundle Item",
                                    filters={"parent": batch["name"]}, 
                                    fields=["serial_no"])
        batch["serial_nos"] = [s["serial_no"] for s in serial_nos]  # Store serial numbers in list

    return batch_records


