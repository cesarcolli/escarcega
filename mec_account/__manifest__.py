# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'MEC Account',
    'version': '1.0.0',
    'category': 'MEC',
    'description': """
MEC Account invoicing
====================================================
    """,
    'depends': ['account'],
    'data': [
        "views/account_invoice_views.xml",
        "security/account_security.xml",
        "security/ir.model.access.csv"
    ],
    'demo': [],
    'installable': True
}
