# Copyright (c) 2025, Vishnu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PackagingBatch(Document):
	def validate(self):
		self.update_total_weight()
	
	def before_insert(self):
		# Generate an auto-incrementing Batch ID
		last_batch = frappe.db.sql("""
			SELECT MAX(CAST(batch_id AS UNSIGNED)) AS max_batch_id
			FROM `tabPackaging Batch`
			WHERE batch_id IS NOT NULL
		""", as_dict=True)

		# Get the last Batch ID and increment it
		max_batch_id = last_batch[0].get("max_batch_id") or 0
		new_batch_id = max_batch_id + 1

		# Set the new Batch ID
		self.batch_id = str(new_batch_id).zfill(6)  # Optional: Zero-padding (e.g., 000001, 000002)

	def update_total_weight(self):
		total_weight = 0.0
		if self.serial_nos:
			for row in self.serial_nos:
				total_weight += row.weight  

		self.weight = total_weight  # Replace 'total_weight' with the actual fieldname in your parent doctype	# Save the changes to the parent doctype

