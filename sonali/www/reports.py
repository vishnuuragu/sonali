import frappe

def get_context(context):
    # Fetch stock details
    stock_details = frappe.db.get_list(
        'Bin',
        fields=['item_code', 'actual_qty', 'warehouse'],
    )

    # Fetch job card details
    job_card_details = frappe.db.get_list(
        'Job Card',
        filters={'status': 'Open'},  # Filter for pending job cards
        fields=['name','operation', 'status', 'employee', 'time_required']
    )

    # Fetch work order details
    work_order_details = frappe.db.get_list(
        'Work Order',
        fields=['name', 'status']
    )

    # Pass the fetched data to the context
    context.stock_details = stock_details
    context.job_card_details = job_card_details
    context.work_order_details = work_order_details
