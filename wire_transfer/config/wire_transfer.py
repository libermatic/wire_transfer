# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Transactions"),
			"items": [
				{
					"type": "doctype",
					"name": "Wire Transaction",
					"description": _("Record wire transactions."),
				},
			]
		},
		{
			"label": _("Reports"),
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Wire Transaction Register",
					"doctype": "Wire Transaction Register",
				},
			]
		},
		{
			"label": _("Setup"),
			"items": [
				{
					"type": "doctype",
					"name": "Wire Account",
					"description": _("Account details."),
				},
				{
					"type": "doctype",
					"name": "Wire Transfer Settings",
					"description": _("Wire transfer configs."),
				},
			]
		},
	]
