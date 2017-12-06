# Copyright (c) 2013, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import add_days

def execute(filters=None):
	column = [
			_("Transaction Date") + ":Date:90",
			_("Document ID") + ":Link/Wire Transaction:90",
			_("Target Account") + ":Link/Wire Account:120",
			_("Account Holder") + ":Link/Wire Account:120",
			_("Customer") + ":Link/Customer:120",
			_("ID Type") + ":Link/Customer:90",
			_("ID No") + ":Link/Customer:90",
			_("Amount") + ":Currency/currency:90",
			_("Charges") + ":Currency/currency:90",
			_("Total") + ":Currency/currency:90",
			_("Outstanding") + ":Currency/currency:90",
		]
	cond = ["wt.docstatus = 1"]
	if filters:
		if filters.get('from_date'):
			cond.append("wt.transaction_date >= '%s'" % filters.get('from_date'))
		if filters.get('to_date'):
			cond.append("wt.transaction_date < '%s'" % add_days(filters.get('to_date'), 1))
		if filters.get('customer'):
			cond.append("wt.customer = '%s'" % filters.get('customer'))
	data = frappe.db.sql("""
		SELECT
			wt.transaction_date,
			wt.name,
			wt.to_account,
			wt.account_holder,
			wt.customer,
			ct.id_type,
			ct.id_no,
			wt.amount,
			wt.charges,
			wt.total,
			wt.total-wt.paid_amount
		FROM `tabWire Transaction` AS wt
		LEFT JOIN `tabCustomer` AS ct ON wt.customer = ct.name
		WHERE {}
		ORDER BY wt.transaction_date
	""".format(" and ".join(cond)))
	return column, data
