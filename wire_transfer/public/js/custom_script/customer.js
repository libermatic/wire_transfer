frappe.ui.form.on('Customer', 'refresh', function(frm) {
  frm.add_custom_button(__('Make Wire Transaction'), function() {
    frm.make_new('Wire Transaction');
  });
});
