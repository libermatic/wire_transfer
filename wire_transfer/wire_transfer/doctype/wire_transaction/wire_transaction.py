# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext import get_default_company
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController

class WireTransaction(AccountsController):
	def on_submit(self):
		self.set_missing_fields()
		self.make_gl_entries()

	def on_cancel(self):
		self.set_missing_fields()
		self.make_gl_entries(cancel=1)

	def set_missing_fields(self):
		self.posting_date = self.transaction_date
		self.company = get_default_company()

	def make_gl_entries(self, cancel=0, adv_adj=0):
		gl_entries = [
			self.get_gl_dict({
					'account': self.debit_account,
					'account_currency': get_account_currency(self.debit_account),
					'debit_in_account_currency': self.amount,
					'debit': self.amount,
					'remarks': "{}".format(self.to_account),
				}),
			self.get_gl_dict({
					'account': self.income_account,
					'account_currency': get_account_currency(self.income_account),
					'debit_in_account_currency': self.charges,
					'debit': self.charges,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center')
				}),
			self.get_gl_dict({
					'account': self.credit_account,
					'account_currency': get_account_currency(self.credit_account),
					'credit_in_account_currency': self.total,
					'credit': self.total,
					'remarks': "{}".format(self.customer),
				}),
		]
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)
