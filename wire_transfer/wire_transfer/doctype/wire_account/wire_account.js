// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wire Account', {
  refresh: function(frm) {
    if (!frm.doc.__islocal) {
      frm.add_custom_button(__('Make Wire Transaction'), function() {
        frm.make_new('Wire Transaction');
      });
    }
  },
});
