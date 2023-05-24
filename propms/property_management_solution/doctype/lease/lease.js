// Copyright (c) 2018, Aakvatech and contributors
// For license information, please see license.txt
cur_frm.add_fetch('property', 'unit_owner', 'property_owner');

frappe.ui.form.on('Lease', {
	setup: function (frm) {
		frm.set_query("lease_item", "lease_item", function () {
			return {
				"filters": [
					["item_group", "=", "Lease Items"],
				]
			};
		});
		frm.set_query("property", function () {
			return {
				"filters": {
					"company": frm.doc.company,
				},
			};
		});
	},
	refresh: function (frm) {
		cur_frm.add_custom_button(__("Make Invoice Schedule"), function () {
			make_lease_invoice_schedule(cur_frm);
		});
		cur_frm.add_custom_button(__("Generate Pending Invoice"), function () {
			generate_pending_invoice();
		});
		cur_frm.add_custom_button(__("Make Invoice Schedule for all Lease"), function () {
			getAllLease(cur_frm);
		});
	},
	onload: function (frm) {
		frappe.realtime.on("lease_invoice_schedule_progress", function (data) {
			if (data.reload && data.reload === 1) {
				frm.reload_doc();
			}
			if (data.progress) {
				let progress_bar = $(cur_frm.dashboard.progress_area).find(".progress-bar");
				if (progress_bar) {
					$(progress_bar).removeClass("progress-bar-danger").addClass("progress-bar-success progress-bar-striped");
					$(progress_bar).css("width", data.progress + "%");
				}
			}
		});
	}
});

var make_lease_invoice_schedule = function (frm) {
	var doc = frm.doc;
	frappe.call({
		method: "propms.property_management_solution.doctype.lease.lease.make_lease_invoice_schedule",
		args: { leasedoc: doc.name },
		callback: function () {
			cur_frm.reload_doc();
		}
	});
};

var generate_pending_invoice = function () {
	frappe.call({
		method: "propms.lease_invoice.leaseInvoiceAutoCreate",
		args: {},
		callback: function () {
			cur_frm.reload_doc();
		}
	});
};

var getAllLease = function () {
	frappe.confirm(
		'Are you sure to initiate this long process?',
		function () {
			frappe.call({
				method: "propms.property_management_solution.doctype.lease.lease.getAllLease",
				args: {},
				callback: function () {
					cur_frm.reload_doc();
				}
			});
		},
		function () {
			frappe.msgprint(__("Closed before starting long process!"));
			window.close();
		}
	);
};

frappe.ui.form.on('Lease Invoice Schedule', {
	create_voucher: function (frm, cdt, cdn) {
		// check if document is saved
		if (frm.is_dirty()) {
			frappe.msgprint("Please save the document first");
			return;
		}
		const row = locals[cdt][cdn];
		if (row.invoice_number || row.sales_order_number) {
			frappe.msgprint("Voucher already created");
			return;
		}
		frappe.call({
			method: "propms.lease_invoice.create_lease_voucher",
			args: {
				invoice_schedule: row,
			},
			callback: function (r) {
				// reload the doc
				frm.reload_doc();
				// refresh child table
				frm.refresh_field("lease_invoice_schedule");
			}
		});

	}
});