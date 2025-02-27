# Copyright (c) 2025, Vishnu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SWWPACKING(Document):
	def validate(self):
		self.update_total_weight()
		self.update_total_length()

	def update_total_weight(self):
		total_weight = 0.0
		if self.sww_table:
			for row in self.sww_table:
				if row.weight:
					total_weight += row.weight  

		self.weight = total_weight  
	def update_total_length(self):
		total_length = 0.0
		if self.sww_table:
				for row in self.sww_table:
					if row.length:
						total_length += row.length  

		self.length = total_length


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
                                   fields=["name", "item_code", "total_qty"])  # Correct field names

    # Fetch serial numbers from "entries" child table in Serial and Batch Bundle
    for batch in batch_records:
        serial_nos = frappe.get_all("Serial and Batch Entry",  # Child table of Serial and Batch Bundle
                                    filters={"parent": batch["name"]}, 
                                    fields=["serial_no"])
        batch["serial_nos"] = [s["serial_no"] for s in serial_nos]  

    return batch_records

