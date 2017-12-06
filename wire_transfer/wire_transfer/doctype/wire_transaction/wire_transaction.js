// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

frappe.ui.form.on('Wire Transaction', {
  refresh: async function(frm) {
    if (frm.doc['docstatus'] === 1) {
      frm.set_df_property('is_paid', 'read_only', 1);
    }
    if (
      frm.doc['docstatus'] === 1 &&
      0 < frm.doc['paid_amount'] &&
      frm.doc['paid_amount'] < frm.doc['total']
    ) {
      const remove_dialog = new frappe.ui.Dialog({
        title: 'Delete Payment',
        fields: [{ fieldname: 'ht', fieldtype: 'HTML' }],
      });
      const container = $('<table />').addClass(
        'table table-condensed table-striped'
      );
      container.append(
        $('<tr />')
          .append($('<th scope="col" />').text('Date'))
          .append($('<th scope="col" class="text-right" />').text('Amount'))
          .append($('<th scope="col" class="text-center" />').text('Action'))
      );
      remove_dialog.fields_dict.ht.$wrapper.append(container);
      frm.doc['payments'].forEach(function({
        payment_id,
        payment_date,
        payment_amount,
      }) {
        const handle_click = async function() {
          const { message = {} } = await frappe.call({
            method:
              'wire_transfer.wire_transfer.doctype.wire_transaction.wire_transaction.make_payment',
            args: {
              name: frm.doc['name'],
              payment_id,
              payment_date,
              payment_amount,
              reverse: 1,
            },
          });
          remove_dialog.hide();
          frm.reload_doc();
        };
        container.append(
          $('<tr />')
            .append($('<td />').text(payment_date))
            .append(
              $('<td class="text-right" />').text(
                format_currency(
                  payment_amount,
                  frappe.defaults.get_default('currency'),
                  2
                )
              )
            )
            .append(
              $('<td class="text-center" />').append(
                $('<i class="fa fa-times" style="cursor: pointer;" />').click(
                  handle_click
                )
              )
            )
        );
      });
      frm.add_custom_button(__('Delete Payment'), async function(fields) {
        remove_dialog.show();
      });
    }
    if (frm.doc['docstatus'] === 1 && !frm.doc['is_paid']) {
      const pay_dialog = new frappe.ui.Dialog({
        title: 'Make Payment',
        fields: [
          {
            label: 'Date',
            fieldname: 'payment_date',
            fieldtype: 'Date',
            default: frappe.datetime.now_date(),
          },
          {
            label: 'Amount',
            fieldname: 'payment_amount',
            fieldtype: 'Currency',
            default: frm.doc['total'] - frm.doc['paid_amount'],
          },
        ],
      });
      pay_dialog.set_primary_action(__('Pay'), async function(fields) {
        await frappe.call({
          method:
            'wire_transfer.wire_transfer.doctype.wire_transaction.wire_transaction.make_payment',
          args: Object.assign(
            { name: frm.doc['name'], payment_id: frappe.utils.get_random(10) },
            fields
          ),
        });
        this.hide();
        frm.reload_doc();
      });
      const pay_button = frm.add_custom_button(
        __('Receive Payment'),
        function() {
          pay_dialog.show();
        }
      );
      pay_button.addClass('btn-primary');
    }
  },
  onload: async function(frm) {
    if (frm.doc.__islocal) {
      frm.add_fetch('to_account', 'account_name', 'account_holder');
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
        frm.set_value('debit_to', default_debit_account);
        frm.set_value('credit_from', default_credit_account);
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
    frm.set_value('total', frm.doc['amount'] + frm.doc['charges']);
  },
  is_paid: async function(frm) {
    if (frm.doc['is_paid']) {
      frm.set_value('paid_amount', frm.doc['total']);
    } else {
      frm.set_value('paid_amount', 0);
    }
  },
  total: async function(frm) {
    const { total, amount } = frm.doc;
    frm.set_value('charges', total - amount);
    if (frm.doc['is_paid']) {
      frm.set_value('paid_amount', total);
    }
  },
});
