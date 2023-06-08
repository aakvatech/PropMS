import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def execute():
    fields={
        "Issue": [
            {
                "fieldname": "column_break_4",
                "fieldtype": "Column Break",
                "insert_after": "subject",
            },
            {
                "fieldname": "property_name",
                "fieldtype": "Link",
                "in_standard_filter": 1,
                "insert_after": "column_break_4",
                "label": "Property Name",
                "options": "Property",
                "reqd": 1,
            },
            {
                "fieldname": "section_break_15",
                "fieldtype": "Section Break",
                "insert_after": "customer",
            },
            {
                "fieldname": "person_in_charge",
                "fieldtype": "Link",
                "in_standard_filter": 1,
                "insert_after": "section_break_15",
                "label": "Person in charge",
                "options": "Employee",
                "reqd": 1,
            },
            {
                "fieldname": "sub_contractor_contact",
                "fieldtype": "Link",
                "insert_after": "person_in_charge",
                "label": "Sub Contractor",
                "options": "Supplier",
            },
            {
                "fieldname": "col_brk_001",
                "fieldtype": "Column Break",
                "insert_after": "sub_contractor_contact",
            },
            {
                "fetch_from": "person_in_charge.employee_name",
                "fieldname": "person_in_charge_name",
                "fieldtype": "Read Only",
                "in_list_view": 1,
                "insert_after": "col_brk_001",
                "label": "Person In Charge Name",
            },
            {
                "fetch_from": "sub_contractor_contact.supplier_name",
                "fieldname": "sub_contractor_name",
                "fieldtype": "Read Only",
                "insert_after": "person_in_charge_name",
                "label": "Sub Contractor Name",
            },
            {
                "fieldname": "column_break_14",
                "fieldtype": "Column Break",
                "insert_after": "description",
            },
            {
                "fieldname": "defect_found",
                "fieldtype": "Text Editor",
                "insert_after": "column_break_14",
                "label": "Defect Found",
            },
            {
                "fieldname": "material_request",
                "fieldtype": "Section Break",
                "insert_after": "defect_found",
                "label": "Material Request",
            },
            {
                "fieldname": "materials_required",
                "fieldtype": "Table",
                "insert_after": "material_request",
                "label": "Materials Required",
                "options": "Issue Materials Detail",
            },
            {
                "fieldname": "materials_billed",
                "fieldtype": "Table",
                "insert_after": "materials_required",
                "label": "Materials Billed",
                "options": "Issue Materials Billed",
                "read_only": 1,
            },
            
            {
                "depends_on": "eval:!doc.__islocal",
                "fieldname": "customer_feedback",
                "fieldtype": "Text Editor",
                "insert_after": "column_break1",
                "label": "Customer Feedback",
            },
        ],
        "Issue Materials Detail": [
            {
                "fieldname": "mateiral_request",
                "fieldtype": "Link",
                "insert_after": "material_status",
                "label": "Mateiral Request",
                "options": "Material Request",
            },   
        ],
        "Quotation": [
            {
                "fieldname": "cost_center",
                "fieldtype": "Link",
                "insert_after": "order_type",
                "label": "Cost Center",
                "options": "Cost Center",
            },
        ],
        "Material Request": [
            {
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
                "insert_after": "job_card",
                "label": "Sales Invoice",
                "options": "Sales Invoice",
            }, 
        ],
        "Material Request Item": [
            {
                "fieldname": "material_request",
                "fieldtype": "Data",
                "insert_after": "page_break",
                "label": "Material Request",
                "translatable": 1,
            },
        ],
        "Item": [
            {
                "description": "If the item requires Gas or Electricity or similar meter reading to charge the customer.",
                "fieldname": "reading_required",
                "fieldtype": "Check",
                "insert_after": "is_sales_item",
                "label": "Reading required",
            },
        ],
        "Company": [
            {
                "fieldname": "property_management_settings",
                "fieldtype": "Section Break",
                "insert_after": "expenses_included_in_valuation",
                "label": "Property Management Settings",
            },
            {
                "fieldname": "security_account_code",
                "fieldtype": "Link",
                "insert_after": "property_management_settings",
                "label": "Security Account Code",
            },
            {
                "fieldname": "default_tax_account_head",
                "fieldtype": "Link",
                "insert_after": "security_account_code",
                "label": "Default Tax Account Head",
            },
            {
                "fieldname": "default_tax_template",
                "fieldtype": "Link",
                "insert_after": "default_tax_account_head",
                "label": "Default Tax Template",
                "options": "Sales Taxes and Charges Template",
            },
            {
                "fieldname": "default_maintenance_tax_template",
                "fieldtype": "Link",
                "insert_after": "default_tax_template",
                "label": "Default Maintenance Tax Template",
                "options": "Sales Taxes and Charges Template",
            },
        ],
        "Sales Invoice": [
            {
                "fieldname": "lease_information",
                "fieldtype": "Section Break",
                "insert_after": "select_print_heading",
                "label": "Lease Information",
            },
            {
                "fieldname": "lease",
                "fieldtype": "Link",
                "insert_after": "lease_information",
                "label": "Lease",
                "options": "Lease",
            },
            {
                "fieldname": "lease_item",
                "fieldtype": "Read Only",
                "insert_after": "lease",
                "label": "Lease Item",
            },
            {
                "fieldname": "job_card",
                "fieldtype": "Link",
                "insert_after": "lease_item",
                "label": "Job Card",
                "options": "Issue",
            }
        ]
    }
    create_custom_fields(fields, update=True) 
  