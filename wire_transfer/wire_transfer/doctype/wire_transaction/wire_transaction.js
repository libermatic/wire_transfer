// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wire Transaction', {
  onload: async function(frm) {
    if (frm.doc.__islocal) {
      frm.set_value('company', frappe.defaults.get_default('Company'));
      const { message } = await frappe.db.get_value(
        'Wire Transfer Settings',
        null,
        [
          'default_debit_account',
          'default_credit_account',
          'default_income_account',
          'default_service_rate',
        ]
      );
      if (message) {
        const {
          default_debit_account,
          default_credit_account,
          default_income_account,
          default_service_rate,
        } = message;
        frm.set_value('debit_account', default_debit_account);
        frm.set_value('credit_account', default_credit_account);
        frm.set_value('income_account', default_income_account);
        frm.set_value('service_rate', default_service_rate);
      }
    }
  },
  amount: async function(frm) {
    frm.set_value(
      'charges',
      frm.doc['amount'] * frm.doc['service_rate'] / 100.0
    );
    frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
  },
  charges: async function(frm) {
    frm.set_value(
      'service_rate',
      frm.doc['charges'] / frm.doc['amount'] * 100.0
    );
    frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
  },
});
