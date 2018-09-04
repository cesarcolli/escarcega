# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    x_requestor_id = fields.Many2one(
        'hr.employee',
        string='Solicita',
        help="Empleado que solicita"
    )

    x_department_id = fields.Many2one(
        'hr.department',
        related='x_requestor_id.department_id',
        string='Departamento',
        help="Departamento solicitante",
        store=True,
        readonly=True
    )

    x_approver_id = fields.Many2one(
        'hr.employee',
        string='Autoriza',
        help="Empleado que autoriza la requisición"
    )

    x_requisition_date = fields.Date(
        string="Fecha de requisición",
        default=fields.Date.context_today,
        required=True,
        copy=False,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help="Fecha de la requisición"
    )

    x_use_on = fields.Text(
        string='Para usar en',
        help="Para que se usarán los materiales o servicios solicitiados"
    )

    @api.onchange('x_requestor_id')
    def onchange_x_requestor_id(self):

        if self.x_requestor_id:
            self.x_department_id = self.x_requestor_id.department_id
            if self.x_department_id and self.x_department_id.manager_id:
                self.x_approver_id = self.x_department_id.manager_id
            else:
                if self.x_requestor_id.parent_id:
                    self.x_approver_id = self.x_requestor_id.parent_id
                else:
                    self.x_approver_id = None

            if self.x_approver_id and self.x_approver_id == self.x_requestor_id:
                self.x_approver_id = self.x_requestor_id.parent_id
            else:
                self.x_approver_id = self.x_approver_id
        else:
            self.x_department_id = None
            self.x_approver_id = None
