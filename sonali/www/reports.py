import frappe

def get_context(context):
    # Fetch stock details
    stock_details = frappe.db.get_list(
        'Bin',
        fields=['item_code', 'actual_qty', 'warehouse'],
    )

    # Fetch job card details
    job_card_details = frappe.db.sql("""
        SELECT 
            jc.name AS name,
            jc.operation AS operation,
            jctl.employee AS employee,
            jc.status AS status,
            jc.time_required AS time_required
        FROM 
            `tabJob Card` jc
        LEFT JOIN 
            `tabJob Card Time Log` jctl
        ON 
            jc.name = jctl.parent
        WHERE 
            jc.status NOT IN ('Completed')
    """, as_dict=True)

    # Fetch work order details
    work_order_details = frappe.db.get_list(
        'Work Order',
        fields=['name', 'status']
    )

    # Pass the fetched data to the context
    context.stock_details = stock_details
    context.job_card_details = job_card_details
    context.work_order_details = work_order_details
