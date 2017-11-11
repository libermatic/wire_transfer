// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wire Transaction', {
	'onload': function(frm, dt, dn) {
		if (frm.doc.__islocal) {
			frappe.call({
		    method: 'frappe.client.get_value',
		    args: {
	        'doctype': 'Wire Transfer Settings',
	        'fieldname': [
						'default_debit_account',
						'default_credit_account',
            'default_income_account',
						'default_service_rate',
	        ]
		    },
		    callback: function(r) {
	        if (!r.exc) {
						const { message : {
							default_debit_account, default_credit_account, default_income_account, default_service_rate,
						} } = r;
						frm.set_value('debit_account', default_debit_account);
						frm.set_value('credit_account', default_credit_account);
						frm.set_value('income_account', default_income_account);
	          frm.set_value('service_rate', default_service_rate);
	        }
		    }
			});
		}
	},
	'amount': function (frm, dt, dn) {
		frm.set_value('charges', frm.doc['amount'] * frm.doc['service_rate'] / 100.0);
		frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
	},
	'charges': function (frm, dt, dn) {
		frm.set_value('service_rate', frm.doc['charges'] / frm.doc['amount'] * 100.0);
		frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
	},
});
