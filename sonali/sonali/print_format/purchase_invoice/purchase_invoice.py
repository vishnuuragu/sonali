def before_save(doc, method):
    if not doc.apply_round_off and doc.custom_manual_rounding is not None:
        doc.rounding_adjustment = doc.custom_manual_rounding
        doc.rounded_total = doc.grand_total + doc.rounding_adjustment
        doc.outstanding_amount = doc.rounded_total - (doc.advance_paid or 0)

        frappe.msgprint(f"Server Updated Outstanding Amount: {doc.outstanding_amount}")
