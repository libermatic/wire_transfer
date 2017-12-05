frappe.listview_settings['Wire Transaction'] = {
  add_fields: ['total', 'paid_amount'],
  get_indicator: function(doc) {
    if (flt(doc['total']) === flt(doc['paid_amount'])) {
      return [__('Paid'), 'green', 'total,=,paid_amount'];
    }
    return [__('Pending'), 'orange', 'total,>,paid_amount'];
  },
};
