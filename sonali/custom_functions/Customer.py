import frappe
import qrcode
from frappe.utils import get_site_path
from frappe.utils.file_manager import save_file


def qr_code(doc, method):
    print("Hello World")
    qr_data = doc.name
    qr_image = qrcode.make(qr_data)  # Create QR code image from serial_no
    qr_code_path = get_site_path("public", "files", f"qr_{doc.name}.png") 
    qr_image.save(qr_code_path)  # Save the image
    doc.custom_qr_image_link = f"/files/qr_{doc.name}.png"