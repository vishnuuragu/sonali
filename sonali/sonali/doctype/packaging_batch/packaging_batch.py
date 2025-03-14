# Copyright (c) 2025, Vishnu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PackagingBatch(Document):
    def validate(self):
        self.update_total_weight()
        self.update_total_length()

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
        total_weight = sum(row.weight for row in self.serial_nos if row.weight)
        self.weight = total_weight

    def update_total_length(self):
        total_length = sum(row.length for row in self.serial_nos if row.length)
        self.length = total_length
        

    def on_submit(self):
        self.create_repack_stock_entry()

    def create_repack_stock_entry(self):
        if not self.serial_nos:
            frappe.throw("No serial numbers found to create a Repack Stock Entry.")

        if not self.item_name:
            frappe.throw("Master Box Item is not set in Packaging Batch.")

        stock_entry = frappe.new_doc("Stock Entry")
        stock_entry.stock_entry_type = "Repack"
        stock_entry.purpose = "Repack"
        stock_entry.set_posting_time = 1
        stock_entry.posting_date = frappe.utils.today()

        source_warehouse = "Stores - S"
        target_warehouse = "Stores - S"

        total_cost = 0  # Calculate total cost based on small box items

        # Add small boxes (raw materials) to be consumed
        for row in self.serial_nos:
            if not row.serial_no or not row.item_code:
                continue

            item_cost = frappe.db.get_value("Item", row.item_code, "valuation_rate") or 0
            total_cost += item_cost

            stock_entry.append("items", {
                "s_warehouse": source_warehouse,
                "item_code": row.item_code,
                "use_serial_batch_fields": 1,
                "serial_no": row.serial_no,
                "qty": 1,  # Each serial no is a unique item
                "uom": "Box",
                "basic_rate": item_cost  # Set cost
            })

        # Add the Master Box (final packed item) to target warehouse
        stock_entry.append("items", {
            "t_warehouse": target_warehouse,
            "item_code": self.item_name,  # Master Box Item
            "qty": 1,  # Only 1 master box per batch
            "uom": "Box",
            "basic_rate": total_cost  # Assign total cost to master box
        })

        stock_entry.insert()
        stock_entry.submit()
        new_serial_no = frappe.db.get_value("Serial No", {"item_code": self.item_name, "warehouse": target_warehouse}, "name",order_by="creation desc")
        if new_serial_no:
             self.master_box_serial = new_serial_no
             self.save()
             frappe.db.set_value("Serial No", new_serial_no, "custom_weight", self.weight)
             frappe.db.commit()
             frappe.msgprint(f"Repack Stock Entry {stock_entry.name} created successfully! Master Box Serial No: {new_serial_no}", alert=True)
        else:
        	frappe.msgprint(f"Repack Stock Entry {stock_entry.name} created successfully!", alert=True)
