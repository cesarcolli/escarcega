# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'MEC Purchase Requisition',
    'version': '1.1.0.27',
    'category': 'MEC',
    'description': """
IQ Purchase Requisition
====================================================
    """,
    'depends': ['purchase_requisition', 'hr'],
    'data': [
        'security/purchase_requisition.xml',
        'security/ir.model.access.csv',
        'views/purchase_requisition_views.xml',
    ],
    'demo': [],
    'installable': True
}
