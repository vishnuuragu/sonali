import frappe

def get_context(context):
    # Fetch stock details
    stock_details = frappe.db.get_list(
        'Bin',
        fields=['item_code', 'actual_qty', 'warehouse'],
    )

    # Fetch job card details (ensure no duplicates by selecting distinct records)
    job_card_details = frappe.db.sql("""
        SELECT DISTINCT
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

    # Optional: Additional deduplication logic in case database query includes duplicates
    unique_job_cards = {}
    for job_card in job_card_details:
        if job_card['name'] not in unique_job_cards:
            unique_job_cards[job_card['name']] = job_card

    # Convert back to a list for rendering in the template
    job_card_details = list(unique_job_cards.values())


    current_page = frappe.form_dict.page or 1  # Get page number from query parameters
    items_per_page = 4
    start = (int(current_page) - 1) * items_per_page

    # Fetch total Work Orders count
    total_count = frappe.db.count('Work Order')

    # Fetch paginated Work Orders
    work_order_details = frappe.db.get_list(
        'Work Order',
        fields=['name', 'status', 'production_item', 'qty'],
        order_by='creation DESC',
        limit_start=start,
        limit_page_length=items_per_page
    )

    # Calculate total pages
    total_pages = (total_count + items_per_page - 1) // items_per_page

    # Pass data to context
    context.work_order_details = work_order_details
    context.current_page = int(current_page)
    context.total_pages = total_pages

    # Pass the fetched data to the context
    context.stock_details = stock_details
    context.job_card_details = job_card_details
    context.work_order_details = work_order_details
