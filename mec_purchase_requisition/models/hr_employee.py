# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    x_requisition_approver = fields.Boolean(
        string='Autoriza requisiciones'
        , help='Marcar si este empleado puede autorizar requisiciones'
    )

    x_requisition_admin = fields.Boolean(
        string='Administra requisiciones'
        , help='Marcar si este empleado puede aministrar requisiciones'
    )
