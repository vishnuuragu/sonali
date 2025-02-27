// Copyright (c) 2025, Vishnu and contributors
// For license information, please see license.txt

// frappe.ui.form.on("HW PACKING", {
// 	refresh(frm) {

// 	},
// });
// frappe.ui.form.on('HW Packing', {
//     work_order: function(frm) {
//         console.log("work_order");
//         if (frm.doc.work_order) {
//             frappe.call({
//                 method: "sonali.sonali.doctype.hw_packing.hw_packing.fetch_stock_entries",  // Check this path
//                 args: {
//                     work_order: frm.doc.work_order
//                 },
//                 callback: function(r) {
//                     if (r.message) {
//                         frm.clear_table("batch_bundle_table"); // Replace with your actual child table fieldname
//                         r.message.forEach(row => {
//                             let child = frm.add_child("batch_bundle_table");
//                             child.batch_no = row.batch_no;
//                             child.item_code = row.item_code;
//                             child.quantity = row.quantity;
//                         });
//                         frm.refresh_field("batch_bundle_table");
//                     }
//                 }
//             });
//         }
//     }
// });
