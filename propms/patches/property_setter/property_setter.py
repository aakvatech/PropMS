import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def execute():
     properties = [
            {
                "doctype": "Property",
                "field_name": "status",
                "property": "options",
                "property_type": "Text",
                "value": "Available\nBooked\nCommon Area (Not for lease)\nManaged for Customer\nOff lease in 3 months\nOn lease\nOn Sale\nRemoved\nRenewal\nSold\nVacating"
            },
            {
                "doctype": "Daily Checklist",
                "property": "default_print_format",
                "property_type": "Data",
                "value": "Viva Daily Checklist"
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "account",
                "property": "columns",
                "property_type": "Int",
                "value": "2"
            },
            {
                "doctype": "Property",
                "field_name": "identification_section",
                "property": "bold",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Property",
                "field_name": "section_break_4",
                "property": "bold",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Property",
                "field_name": "section_break_13",
                "property": "bold",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Property",
                "field_name": "section_break_22",
                "property": "bold",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "section_break_7",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Issue",
                "field_name": "section_break_19",
                "property": "collapsible",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Issue",
                "field_name": "raised_by",
                "property": "report_hide",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "email_account",
                "property": "report_hide",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "issue_type",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "priority",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Lease",
                "field_name": "property_owner",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "customer",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "start_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "end_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Unit Type",
                "property": "search_fields",
                "property_type": "Data",
                "value": "unit_type"
            },
            {
                "doctype": "Issue",
                "field_name": "opening_date",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "raised_by",
                "property": "in_list_view",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Issue",
                "field_name": "issue_type",
                "property": "reqd",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "status",
                "property": "options",
                "property_type": "Text",
                "value": "Open\nIn Progress\nAwaiting Parts\nUnder Observation\nIn Discussion\nAppointment\nHold\nClosed"
            },
            {
                "doctype": "Contact",
                "field_name": "department",
                "property": "fieldtype",
                "property_type": "Select",
                "value": "Select"
            },
            {
                "doctype": "Contact",
                "field_name": "department",
                "property": "options",
                "property_type": "Text",
                "value": "\nOutsourcing - Cleaning"
            },
            {
                "doctype": "Material Request",
                "field_name": "material_request_type",
                "property": "options",
                "property_type": "Text",
                "value": "Material Issue\nPurchase\nMaterial Transfer\nManufacture"
            },
            {
                "doctype": "Key Set Detail",
                "field_name": "taken_by",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Key Set Detail",
                "field_name": "returned",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Key Set Detail",
                "field_name": "key_set",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "property_owner",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "lease_customer",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "customer",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "property_user",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "security_status",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "property",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "wtax_paid_by",
                "property": "in_standard_filter",
                "property_type": "Check",
                "value": "1"
            },
            {
                "doctype": "Lease",
                "field_name": "security_status",
                "property": "options",
                "property_type": "Text",
                "value": "\nProforma Invoice raised\nReceiving in process\nReceived\nReceived in part\nReturn in part\nReturned\nRecovered for rent\nRecovered for repairs\nNot required"
            },
            {
                "doctype": "Issue",
                "property": "quick_entry",
                "property_type": "Check",
                "value": "0"
            },
            {
                "doctype": "Journal Entry Account",
                "field_name": "cost_center",
                "property": "columns",
                "property_type": "Int",
                "value": "1"
            },
            {
                "doctype": "Issue",
                "field_name": "company",
                "property": "fetch_from",
                "property_type": "Small Text",
                "value": "property_name.company"
            }

     ]
     for property in properties:
        make_property_setter(
            property.get("doctype"),
            property.get("fieldname"),
            property.get("property"),
            property.get("value"),
            property.get("property_type"),
            for_doctype=False,
            validate_fields_for_doctype=False
        )

frappe.db.commit()          