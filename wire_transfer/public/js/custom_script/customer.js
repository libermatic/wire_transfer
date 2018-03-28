frappe.ui.form.on('Customer', 'refresh', function(frm) {
  const button_label = 'Make Wire Transaction';
  if (
    !frm.doc.__islocal &&
    !frm.custom_buttons[button_label] &&
    frm.doc.utility_service.length > 0
  ) {
    frm.add_custom_button(__(button_label), function() {
      frm.make_new('Wire Transaction');
    });
  }
});
