import frappe

def flush_stock_entries():
    # Delete Stock Entries and Related Records
    frappe.db.sql("DELETE FROM `tabStock Entry`")
    frappe.db.sql("DELETE FROM `tabStock Entry Detail`")
    
    # Delete Work Orders
    frappe.db.sql("DELETE FROM `tabWork Order`")
    frappe.db.sql("DELETE FROM `tabWork Order Item`")

    # Delete Ledger and GL Entries
    frappe.db.sql("DELETE FROM `tabStock Ledger Entry`")  # Clears stock movements
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE voucher_type IN ('Stock Entry', 'Work Order')")
    
    # Delete Serial Numbers & Batch Numbers
    frappe.db.sql("DELETE FROM `tabSerial No`")
    frappe.db.sql("DELETE FROM `tabBatch`")

    # Reset Bin table (Current Stock Levels)
    frappe.db.sql("DELETE FROM `tabBin`")

    frappe.db.commit()
    print("All Stock Entries, Work Orders, Serial Numbers, Batches, and Bin Data have been flushed.")

def flush_sales_invoices():
    frappe.db.sql("DELETE FROM `tabSales Invoice`")
    frappe.db.sql("DELETE FROM `tabSales Invoice Item`")
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE voucher_type = 'Sales Invoice'")
    frappe.db.commit()
    print("Sales Invoices Flushed Successfully.")