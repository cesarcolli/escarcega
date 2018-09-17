# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, tools, models, _


class ProductUoM(models.Model):
    _inherit = "product.uom"

    @api.multi
    def _compute_quantity(self, qty, to_unit, round=True, rounding_method='UP'):
        if not self:
            return qty
        self.ensure_one()

        if self.category_id.id != to_unit.category_id.id:
            return qty

        amount = qty / self.factor
        if to_unit:
            amount = amount * to_unit.factor
            if round:
                amount = tools.float_round(amount, precision_rounding=to_unit.rounding, rounding_method=rounding_method)
        return amount
