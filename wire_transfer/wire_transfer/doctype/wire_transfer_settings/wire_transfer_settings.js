// Copyright (c) 2017, Libermatic and contributors
// For license information, please see license.txt

cur_frm.fields_dict['default_debit_account'].get_query = function(doc) {
  return {
    filters: {
      account_type: 'Bank',
      is_group: false,
    },
  };
};

cur_frm.fields_dict['default_credit_account'].get_query = function(doc) {
  return {
    filters: {
      account_type: 'Cash',
      is_group: false,
    },
  };
};

cur_frm.fields_dict['default_income_account'].get_query = function(doc) {
  return {
    filters: {
      root_type: 'Income',
      is_group: false,
    },
  };
};
