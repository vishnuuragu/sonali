import frappe

def get_context(context):
    # Fetch stock details
    stock_details = frappe.db.get_list(
        'Bin',
        fields=['item_code', 'actual_qty', 'warehouse'],
    )
    # Pass the fetched data to the context
    context.stock_details = stock_details

    # For Work Orders and Job Cards combined report
    work_orders = frappe.db.get_list(
        'Work Order',
        fields=['name', 'status', 'production_item', 'qty'],
        order_by='creation DESC',
        limit_page_length=1
    )

    # Combine Work Orders with related Job Cards and calculate progress
    combined_data = []
    for work_order in work_orders:
        # Fetch related Job Cards
        job_cards = frappe.db.sql("""
            SELECT DISTINCT
                jc.operation AS operation,
                jctl.employee AS employee,
                jc.status AS status
            FROM 
                `tabJob Card` jc
            LEFT JOIN 
                `tabJob Card Time Log` jctl
            ON 
                jc.name = jctl.parent
            WHERE 
                jc.work_order = %s
        """, work_order.name, as_dict=True)

        # Calculate progress (percentage of completed operations)
        total_operations = len(job_cards)
        completed_operations = sum(1 for jc in job_cards if jc['status'] == 'Completed')
        progress = (completed_operations / total_operations * 100) if total_operations > 0 else 0

        # Add to combined data
        combined_data.append({
            'name': work_order.name,
            'status': work_order.status,
            'production_item': work_order.production_item,
            'qty': work_order.qty,
            'progress': int(progress),
            'operations': job_cards
        })

    # Pass data to context
    context.combined_data = combined_data

    # Fetch outstanding sales orders
    outstanding_sales_orders = frappe.db.get_list(
        'Sales Order',
        filters={
            'status': ['not in', ['Completed', 'Cancelled']],
            'docstatus': 1  # Ensure the sales order is submitted
        },
        fields=['name', 'customer', 'transaction_date', 'grand_total', 'status','delivery_date']
    )
    context.outstanding_sales_orders = outstanding_sales_orders

    # Fetch outstanding amounts for each customer
    customer_outstanding = frappe.db.sql(
        """
        SELECT 
            customer, 
            SUM(outstanding_amount) AS outstanding_total,
            name,
            status
        FROM 
            `tabSales Invoice`
        WHERE 
            docstatus = 1 AND outstanding_amount > 0
        GROUP BY 
            customer
        """,
        as_dict=True
    )
    context.customer_outstanding = customer_outstanding

    # Fetch pending tasks and assigned users
    pending_tasks = frappe.db.get_list(
        'Task',
        filters={
            'status': ['not in', ['Completed', 'Cancelled']]
        },
        fields=['type', 'exp_end_date', 'status', 'assigned_to']
    )
    context.pending_tasks = pending_tasks
