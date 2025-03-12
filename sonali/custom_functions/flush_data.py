import frappe

def flush_stock_entries():
    frappe.db.sql("DELETE FROM `tabStock Entry`")
    frappe.db.sql("DELETE FROM `tabStock Entry Detail`")
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE voucher_type = 'Stock Entry'")
    frappe.db.sql("DELETE FROM `tabStock Ledger Entry`")
    frappe.db.commit()
    print("All Stock Entries and Ledger Entries Flushed Successfully.")

def flush_sales_invoices():
    frappe.db.sql("DELETE FROM `tabSales Invoice`")
    frappe.db.sql("DELETE FROM `tabSales Invoice Item`")
    frappe.db.sql("DELETE FROM `tabGL Entry` WHERE voucher_type = 'Sales Invoice'")
    frappe.db.commit()
    print("Sales Invoices Flushed Successfully.")