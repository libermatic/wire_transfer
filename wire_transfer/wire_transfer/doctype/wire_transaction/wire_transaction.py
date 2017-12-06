# -*- coding: utf-8 -*-
# Copyright (c) 2017, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, random_string
from erpnext.accounts.party import get_party_account
from erpnext.accounts.utils import get_account_currency
from erpnext.accounts.general_ledger import make_gl_entries
from erpnext.controllers.accounts_controller import AccountsController

class WireTransaction(AccountsController):
	def before_submit(self):
		if self.is_paid:
			self.append('payments', {
					'payment_id': random_string(10),
					'payment_date': self.transaction_date,
					'payment_amount': self.paid_amount
				})

	def on_submit(self):
		self.set_missing_fields()
		self.make_parent_gl_entries()

	def on_cancel(self):
		self.set_missing_fields()
		for entry in self.payments:
				make_payment(
				self.name,
				payment_id=entry.payment_id,
				payment_date=entry.payment_date,
				payment_amount=entry.payment_amount,
				parent_cancel=1
			)
		self.make_parent_gl_entries(cancel=1)

	def before_update_after_submit(self):
		total_paid = 0.0
		for row in self.payments:
			total_paid += flt(row.get_value('payment_amount'))
			if total_paid > self.total:
				return frappe.throw(_("Total paid amount cannot be greater than invoiced amount"))
		self.paid_amount = total_paid
		if total_paid == self.total:
			self.is_paid = 1

	def set_missing_fields(self):
		self.posting_date = self.transaction_date

	def make_parent_gl_entries(self, cancel=0, adv_adj=0):
		party_account = get_party_account('Customer', self.customer, self.company)
		gl_entries = [
			self.get_gl_dict({
					'account': self.credit_from,
					'account_currency': get_account_currency(self.credit_from),
					'credit_in_account_currency': self.amount,
					'credit': self.amount,
					'against': self.to_account,
				}),
			self.get_gl_dict({
					'account': self.income_account,
					'account_currency': get_account_currency(self.income_account),
					'credit_in_account_currency': self.charges,
					'credit': self.charges,
					'cost_center': frappe.db.get_value('Company', self.company, 'cost_center'),
					'against': self.customer,
				}),
			self.get_gl_dict({
					'account': party_account,
					'account_currency': get_account_currency(party_account),
					'debit_in_account_currency': self.total,
					'debit': self.total,
					'party_type': 'Customer',
					'party': self.customer,
				}),
		]
		if self.is_paid:
			gl_entries.append(self.get_gl_dict({
					'account': party_account,
					'account_currency': get_account_currency(party_account),
					'credit_in_account_currency': self.total,
					'credit': self.total,
					'party_type': 'Customer',
					'party': self.customer,
					'against': self.debit_to,
				}))
			gl_entries.append(self.get_gl_dict({
					'account': self.debit_to,
					'account_currency': get_account_currency(self.debit_to),
					'debit_in_account_currency': self.total,
					'debit': self.total,
					'against': self.customer,
				}))
		make_gl_entries(gl_entries, cancel=cancel, adv_adj=adv_adj)


@frappe.whitelist()
def make_payment(name, payment_id, payment_date, payment_amount, reverse=0, parent_cancel=0):
	r = frappe.get_doc('Wire Transaction', name)
	cancel = reverse or parent_cancel
	if cancel:
		for entry in r.payments:
			if entry.get_value('payment_id') == payment_id:
				r.remove(entry)
				break
	else:
		r.append('payments', {
				'payment_id': payment_id,
				'payment_date': payment_date,
				'payment_amount': payment_amount
			})
	if not parent_cancel:
		r.save()
	r.posting_date = payment_date
	r.company = get_default_company()
	party_account = get_party_account('Customer', r.customer, r.company)
	gl_entries = [
		r.get_gl_dict({
				'account': party_account,
				'account_currency': get_account_currency(party_account),
				'credit_in_account_currency': payment_amount,
				'credit': payment_amount,
				'voucher_type': 'Wire Transaction Payment',
				'voucher_no': payment_id,
				'party_type': 'Customer',
				'party': r.customer,
				'against': r.debit_to,
				'against_voucher_type': 'Wire Transaction',
				'against_voucher': name,
			}),
		r.get_gl_dict({
				'account': r.debit_to,
				'account_currency': get_account_currency(r.debit_to),
				'debit_in_account_currency': payment_amount,
				'debit': payment_amount,
				'voucher_type': 'Wire Transaction Payment',
				'voucher_no': payment_id,
				'against': r.customer,
			}),
	]
	make_gl_entries(gl_entries, cancel=cancel, adv_adj=0)
