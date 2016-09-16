import frappe
from frappe import _

def execute():
	from erpnext.setup.setup_wizard.install_fixtures import default_lead_sources

	frappe.reload_doc('selling', 'doctype', 'lead_source')

	frappe.local.lang = frappe.db.get_default("lang") or 'en'

	for s in default_lead_sources:
		frappe.get_doc(dict(doctype='Lead Source', source_name=_(s))).insert()

	# get lead sources in existing forms (customized)
	# and create a document if not created
	for d in ['Lead', 'Opportunity', 'Quotation', 'Sales Order', 'Delivery Note', 'Sales Invoice']:
		sources = frappe.db.sql_list('select distinct source from `tab{0}`'.format(d))
		for s in sources:
			if s and s not in default_lead_sources:
				frappe.get_doc(dict(doctype='Lead Source', source_name=s)).insert()
