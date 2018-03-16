# -*- coding: utf-8 -*-
# Copyright (c) 2018, Libermatic and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def _set_fixtures():
    # for custom field
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Customer',
            'label': 'ID Information',
            'fieldname': 'id_information',
            'fieldtype': 'Section Break',
            'insert_after': 'language',
            'collapsible': 1,
        }).insert(ignore_if_duplicate=True)
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Customer',
            'label': 'ID Type',
            'fieldname': 'id_type',
            'fieldtype': 'Select',
            'insert_after': 'id_information',
            'options': '\nAadhaar\nDriving License\nPAN\nPassport\nVoter ID',
        }).insert(ignore_if_duplicate=True)
    frappe.get_doc({
            'doctype': 'Custom Field',
            'dt': 'Customer',
            'label': 'ID No',
            'fieldname': 'id_no',
            'fieldtype': 'Data',
            'insert_after': 'id_type',
        }).insert(ignore_if_duplicate=True)


def after_install(args=None):
    _set_fixtures()
