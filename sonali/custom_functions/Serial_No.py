import frappe
import qrcode
from frappe.utils import get_site_path
from frappe.utils.file_manager import save_file
import random
import string


def generate_id(length=12):
    char_set = string.ascii_letters + string.digits
    return ''.join(random.SystemRandom().choice(char_set) for _ in range(length))

@frappe.whitelist()
def generate_qr_for_missing_serials():
    missing_qr_serials = frappe.get_all('Serial No', filters={'custom_qr_image_link': ['is', 'not set']})
    
    for serial in missing_qr_serials:
        # Get the Serial No document
        serial_doc = frappe.get_doc('Serial No', serial.name)
        generate_qr_code(serial_doc)  # Generate QR code for this Serial No

def generate_qr_code(serial_no_doc):
    print(f"Generating QR code for Serial No: {serial_no_doc.serial_no}")
    serial_no_doc.custom_uuid = generate_id()
    qr_data = serial_no_doc.custom_uuid
    qr_image = qrcode.make(qr_data)  # Create QR code image from serial_no
    qr_code_path = get_site_path("public", "files", f"qr_{serial_no_doc.serial_no}.png")  # Path to save image
    qr_image.save(qr_code_path)  # Save the image
    serial_no_doc.custom_qr_image_link = f"/files/qr_{serial_no_doc.serial_no}.png"  # Link to the saved QR code
      # Generate a random UUID
    serial_no_doc.save()  # Save the Serial No record with the new qr_code_link
    print(f"QR code saved at {qr_code_path}")
