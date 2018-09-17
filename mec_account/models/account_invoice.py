# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    to_pay = fields.Boolean(
        string='Pago autorizado',
        readonly=True,
        default=False,
        help="Este campo será marcado cuando el director aprueba esta factura para ser pagada")

    @api.one
    def copy(self, default=None):
        default = default or {}
        default.update({
            'to_pay': False,
        })
        return super(AccountInvoice, self).copy(default)

    @api.multi
    def payment_approve(self):
        return self.write({'to_pay': True})

    @api.multi
    def payment_disapproves(self):
        return self.write({'to_pay': False})

    @api.multi
    def payment_register(self):
        payment_form = self.env.ref('account.view_account_payment_invoice_form', False)
        return {
            'name': 'Register Payment',
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'views': [(payment_form.id, 'form')],
            'view_id': payment_form.id,
            'context': {'default_invoice_ids': [(4, self.id, None)]}
        }
