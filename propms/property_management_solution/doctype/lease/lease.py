# -*- coding: utf-8 -*-
# Copyright (c) 2018, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today, getdate, add_months, get_datetime, now
from propms.auto_custom import app_error_log, makeInvoiceSchedule, getDateMonthDiff


class Lease(Document):
    def on_submit(self):
        try:
            checklist_doc = frappe.get_doc("Checklist Checkup Area", "Handover")
            if checklist_doc:
                check_list = []
                for task in checklist_doc.task:
                    check = {}
                    check["checklist_task"] = task.task_name
                    check_list.append(check)

                frappe.get_doc(
                    dict(
                        doctype="Daily Checklist",
                        area="Handover",
                        checkup_date=self.start_date,
                        daily_checklist_detail=check_list,
                        property=self.property,
                    )
                ).insert()
        except Exception as e:
            app_error_log(frappe.session.user, str(e))

    def validate(self):
        try:
            if (
                get_datetime(self.start_date)
                <= get_datetime(now())
                <= get_datetime(add_months(self.end_date, -3))
            ):
                frappe.db.set_value("Property", self.property, "status", "On Lease")
                frappe.msgprint("Property set to On Lease")
            if (
                get_datetime(add_months(self.end_date, -3))
                <= get_datetime(now())
                <= get_datetime(add_months(self.end_date, 3))
            ):
                frappe.db.set_value(
                    "Property", self.property, "status", "Off Lease in 3 Months"
                )
                frappe.msgprint("Property set to Off Lease in 3 Months")
        except Exception as e:
            app_error_log(frappe.session.user, str(e))


@frappe.whitelist()
def getAllLease():
    # Below is temporarily created to manually run through all lease and refresh lease invoice schedule. Hardcoded to start from 1st Jan 2020.
    frappe.msgprint(
        "The task of making lease invoice schedule for all users has been sent for background processing."
    )
    invoice_start_date = frappe.db.get_single_value(
        "Property Management Settings", "invoice_start_date"
    )
    lease_list = frappe.get_all(
        "Lease", filters={"end_date": (">=", invoice_start_date)}, fields=["name"]
    )
    # frappe.msgprint("Working on lease_list" + str(lease_list))
    lease_list_len = len(lease_list)
    frappe.msgprint("Total number of lease to be processed is " + str(lease_list_len))
    for lease in lease_list:
        make_lease_invoice_schedule(lease.name)


# def on_update(self):
@frappe.whitelist()
def make_lease_invoice_schedule(leasedoc):
    # frappe.msgprint("This is the parameter passed: " + str(leasedoc))
    lease = frappe.get_doc("Lease", str(leasedoc))
    try:
        # Delete unnecessary records after lease end date
        lease_invoice_schedule_list = frappe.get_list(
            "Lease Invoice Schedule",
            fields=[
                "name",
                "parent",
                "lease_item",
                "invoice_number",
                "date_to_invoice",
            ],
            filters={"parent": lease.name, "date_to_invoice": (">", lease.end_date)}, parent_doctype='Lease',
        )
        for lease_invoice_schedule in lease_invoice_schedule_list:
            frappe.delete_doc("Lease Invoice Schedule", lease_invoice_schedule.name)
        # Only process lease that items and is current
        if len(lease.lease_item) >= 1 and lease.end_date >= getdate(today()):
            # Clean up records that are no longer required, i.e. of unnecessary lease items and unnecessary dates
            # Records before Invoice Start Date
            invoice_start_date = frappe.db.get_single_value(
                "Property Management Settings", "invoice_start_date"
            )
            lease_invoice_schedule_list = frappe.get_list(
                "Lease Invoice Schedule",
                fields=["name", "parent", "invoice_number", "date_to_invoice"],
                filters={
                    "parent": lease.name,
                    "date_to_invoice": ("<", invoice_start_date),
                }, parent_doctype='Lease',
            )
            # frappe.msgprint("Records before Invoice Start Date " + str(lease_invoice_schedule_list))
            for lease_invoice_schedule in lease_invoice_schedule_list:
                # frappe.msgprint("Deleting Record before Invoice Start Date " + str(invoice_start_date) + str(lease_invoice_schedule.name))
                frappe.delete_doc("Lease Invoice Schedule", lease_invoice_schedule.name)
            # Records of lease_items that no longer existing in lease.lease_item
            lease_invoice_schedule_list = frappe.get_list(
                "Lease Invoice Schedule",
                fields=[
                    "name",
                    "parent",
                    "lease_item",
                    "invoice_number",
                    "date_to_invoice",
                ],
                filters={"parent": lease.name}, parent_doctype='Lease',
            )
            lease_items_list = frappe.get_list(
                "Lease Item",
                fields=["name", "parent", "lease_item"],
                filters={"parent": lease.name}, parent_doctype='Lease',
            )
            # Create list of lease items that are part of lease.lease_item
            lease_item_name_list = [
                lease_item["lease_item"] for lease_item in lease_items_list
            ]
            # frappe.msgprint(str(lease_item_list))
            for lease_invoice_schedule in lease_invoice_schedule_list:
                if lease_invoice_schedule.lease_item not in lease_item_name_list:
                    # frappe.msgprint("This lease item will be removed from invoice schedule " + str(lease_invoice_schedule.lease_item))
                    frappe.delete_doc(
                        "Lease Invoice Schedule", lease_invoice_schedule.name
                    )
            item_invoice_frequency = {
                "Monthly": 1.00,  # .00 to make it float type
                "Bi-Monthly": 2.00,
                "Quarterly": 3.00,
                "6 months": 6.00,
                "Annually": 12.00,
            }
            idx = 1
            for item in lease.lease_item:
                # frappe.msgprint("Lease item being processed: " + str(item.lease_item))
                lease_invoice_schedule_list = frappe.get_all(
                    "Lease Invoice Schedule",
                    fields=[
                        "name",
                        "parent",
                        "lease_item",
                        "qty",
                        "invoice_number",
                        "date_to_invoice",
                    ],
                    filters={"parent": lease.name, "lease_item": item.lease_item},
                    order_by="date_to_invoice",
                )
                # frappe.msgprint(str(lease_invoice_schedule_list))
                # Get the latest item frequency incase lease was changed.
                frequency_factor = item_invoice_frequency.get(
                    item.frequency, "Invalid frequency"
                )
                # frappe.msgprint("Next Invoice date calculated: " + str(invoice_date))
                if frequency_factor == "Invalid frequency":
                    message = (
                        "Invalid frequency: "
                        + str(item.frequency)
                        + " for "
                        + str(leasedoc)
                        + " not found. Contact the developers!"
                    )
                    frappe.log_error("Frequency incorrect", message)
                    break
                invoice_qty = float(frequency_factor)
                end_date = lease.end_date
                invoice_date = lease.start_date
                # Find out the first invoice date on or after Invoice Start Date process.
                while end_date >= invoice_date and invoice_date < invoice_start_date:
                    invoice_period_end = add_days(
                        add_months(invoice_date, frequency_factor), -1
                    )
                    # Set invoice_Qty as appropriate fraction of frequency_factor
                    if invoice_period_end > end_date:
                        invoice_qty = getDateMonthDiff(invoice_date, end_date, 1)
                        # frappe.msgprint("Invoice quantity corrected as " + str(invoice_qty))
                    invoice_date = add_days(invoice_period_end, 1)
                # If there is no lease_invoice_schedule_list found, i.e. it is fresh new list to be created
                if not lease_invoice_schedule_list:
                    while end_date >= invoice_date:
                        invoice_period_end = add_days(
                            add_months(invoice_date, frequency_factor), -1
                        )
                        # frappe.msgprint("Invoice period end: " + str(invoice_period_end) + "--- Invoice Date: " + str(invoice_date))
                        # frappe.msgprint("End Date: " + str(end_date))
                        # set invoice_Qty as appropriate fraction of frequency_factor
                        if invoice_period_end > end_date:
                            invoice_qty = getDateMonthDiff(invoice_date, end_date, 1)
                            # frappe.msgprint("Invoice quantity corrected as " + str(invoice_qty))
                        # frappe.msgprint("Making Fresh Invoice Schedule for " + str(invoice_date)
                        # 	+ ", Quantity calculated: " + str(invoice_qty))
                        makeInvoiceSchedule(
                            invoice_date,
                            item.lease_item,
                            item.paid_by,
                            item.lease_item,
                            lease.name,
                            invoice_qty,
                            item.amount,
                            idx,
                            item.currency_code,
                            item.witholding_tax,
                            lease.days_to_invoice_in_advance,
                            item.invoice_item_group,
                            item.document_type,
                        )
                        idx += 1
                        invoice_date = add_days(invoice_period_end, 1)
                for lease_invoice_schedule in lease_invoice_schedule_list:
                    # frappe.msgprint("Upon entering lease_invoice_schedule_list - Date to invoice: " + str(lease_invoice_schedule.date_to_invoice)
                    # 	+ " and invoice date to process is " + str(invoice_date))
                    if not (lease_invoice_schedule.schedule_start_date):
                        lease_invoice_schedule.schedule_start_date = (
                            lease_invoice_schedule.date_to_invoice
                        )
                    while (
                        end_date >= invoice_date
                        and lease_invoice_schedule.schedule_start_date > invoice_date
                    ):
                        invoice_period_end = add_days(
                            add_months(invoice_date, frequency_factor), -1
                        )
                        # frappe.msgprint("Upon entering Invoice period end: " + str(invoice_period_end) + "--- Invoice Date: " + str(invoice_date))
                        # frappe.msgprint("End Date: " + str(end_date))
                        # set invoice_Qty as appropriate fraction of frequency_factor
                        if invoice_period_end > end_date:
                            invoice_qty = getDateMonthDiff(invoice_date, end_date, 1)
                            # frappe.msgprint("Invoice quantity corrected as " + str(invoice_qty))
                        # frappe.msgprint("Making Pre Invoice Schedule for " + str(invoice_date) + ", Quantity calculated: " + str(invoice_qty))
                        makeInvoiceSchedule(
                            invoice_date,
                            item.lease_item,
                            item.paid_by,
                            item.lease_item,
                            lease.name,
                            invoice_qty,
                            item.amount,
                            idx,
                            item.currency_code,
                            item.witholding_tax,
                            lease.days_to_invoice_in_advance,
                            item.invoice_item_group,
                            item.document_type,
                        )
                        idx += 1
                        invoice_date = add_days(invoice_period_end, 1)
                    # frappe.msgprint(str(lease_invoice_schedule))
                    # If the record already exists and invoice is generated
                    if (
                        lease_invoice_schedule.invoice_number is not None
                        and lease_invoice_schedule.invoice_number != ""
                    ):
                        # frappe.msgprint("Lease Invoice Schedule retained: " + lease_invoice_schedule.name
                        # 	+ " for invoice number: " + str(lease_invoice_schedule.invoice_number)
                        # 	+ " dated " + str(lease_invoice_schedule.date_to_invoice)
                        # )
                        # Set months as rounded up by 1 if the month is a fraction (last invoice for the lease item already created).
                        # Above needed to escape from infinite loop of rounded down date and therefore never reaching end of the lease.
                        if lease_invoice_schedule.qty != round(
                            lease_invoice_schedule.qty, 0
                        ):
                            add_months_value = round(lease_invoice_schedule.qty, 0) + 1
                        else:
                            add_months_value = lease_invoice_schedule.qty
                        # frappe.msgprint("Add Months Value" + str(add_months_value) + " due to qty = " + str(lease_invoice_schedule.qty))
                        invoice_date = add_months(
                            lease_invoice_schedule.schedule_start_date, add_months_value
                        )
                        # Set sequence to show it on the top
                        frappe.db.set_value(
                            "Lease Invoice Schedule",
                            lease_invoice_schedule.name,
                            "idx",
                            idx,
                        )
                        idx += 1
                    # If the invoice is not created
                    else:
                        # frappe.msgprint("Deleting schedule :" + lease_invoice_schedule.name + " dated: " + str(lease_invoice_schedule.date_to_invoice) + " for " + str(lease_invoice_schedule.lease_item))
                        frappe.delete_doc(
                            "Lease Invoice Schedule", lease_invoice_schedule.name
                        )
                # frappe.msgprint("first invoice_date: " + str(invoice_date), "Lease Invoice Schedule")
                while end_date >= invoice_date:
                    invoice_period_end = add_days(
                        add_months(invoice_date, frequency_factor), -1
                    )
                    # frappe.msgprint("Invoice period end: " + str(invoice_period_end) + "--- Invoice Date: " + str(invoice_date))
                    # frappe.msgprint("End Date: " + str(end_date))
                    # set invoice_Qty as appropriate fraction of frequency_factor
                    if invoice_period_end > end_date:
                        invoice_qty = getDateMonthDiff(invoice_date, end_date, 1)
                        # frappe.msgprint("Invoice quantity corrected as " + str(invoice_qty))
                    # frappe.msgprint("Making Post Invoice Schedule for " + str(invoice_date) + ", Quantity calculated: " + str(invoice_qty))
                    makeInvoiceSchedule(
                        invoice_date,
                        item.lease_item,
                        item.paid_by,
                        item.lease_item,
                        lease.name,
                        invoice_qty,
                        item.amount,
                        idx,
                        item.currency_code,
                        item.witholding_tax,
                        lease.days_to_invoice_in_advance,
                        item.invoice_item_group,
                        item.document_type,
                    )
                    idx += 1
                    invoice_date = add_days(invoice_period_end, 1)

        frappe.msgprint("Completed making of invoice schedule.")

    except Exception as e:
        frappe.msgprint("Exception error! Check app error log.")
        app_error_log(frappe.session.user, str(e))
