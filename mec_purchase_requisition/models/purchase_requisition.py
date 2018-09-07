# -*- coding: utf-8 -*-
# © <2018> <IDEANET (cesarcolli@ideanet.com.mx)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    x_requestor_id = fields.Many2one(
        'hr.employee',
        string='Solicita',
        help="Empleado que solicita",
        required=True
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
        help="Empleado que autoriza la requisición",
        required=True
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


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    name = fields.Text(string='Descripción', required=False)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        super(PurchaseRequisitionLine, self)._onchange_product_id()

        if not self.product_id:
            self.name = None
            return

        self.name = self.product_id.display_name


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange('requisition_id')
    def _onchange_requisition_id(self):
        if not self.requisition_id:
            return

        requisition = self.requisition_id
        if self.partner_id:
            partner = self.partner_id
        else:
            partner = requisition.vendor_id
        payment_term = partner.property_supplier_payment_term_id
        currency = partner.property_purchase_currency_id or requisition.company_id.currency_id

        FiscalPosition = self.env['account.fiscal.position']
        fpos = FiscalPosition.get_fiscal_position(partner.id)
        fpos = FiscalPosition.browse(fpos)

        self.partner_id = partner.id
        self.fiscal_position_id = fpos.id
        self.payment_term_id = payment_term.id,
        self.company_id = requisition.company_id.id
        self.currency_id = currency.id
        if not self.origin or requisition.name not in self.origin.split(', '):
            if self.origin:
                if requisition.name:
                    self.origin = self.origin + ', ' + requisition.name
            else:
                self.origin = requisition.name
        self.notes = requisition.description
        self.date_order = requisition.date_end or fields.Datetime.now()
        self.picking_type_id = requisition.picking_type_id.id

        if requisition.type_id.line_copy != 'copy':
            return

        # Create PO lines if necessary
        order_lines = []
        for line in requisition.line_ids:
            # Compute name
            product_lang = line.product_id.with_context({
                'lang': partner.lang,
                'partner_id': partner.id,
            })

            name = product_lang.display_name
            if line.name:
                name = line.name

            if product_lang.description_purchase:
                name += '\n' + product_lang.description_purchase

            # Compute taxes
            if fpos:
                taxes_ids = fpos.map_tax(line.product_id.supplier_taxes_id.filtered(
                    lambda tax: tax.company_id == requisition.company_id)).ids
            else:
                taxes_ids = line.product_id.supplier_taxes_id.filtered(
                    lambda tax: tax.company_id == requisition.company_id).ids

            # Compute quantity and price_unit
            if line.product_uom_id != line.product_id.uom_po_id:
                product_qty = line.product_uom_id._compute_quantity(line.product_qty, line.product_id.uom_po_id)
                price_unit = line.product_uom_id._compute_price(line.price_unit, line.product_id.uom_po_id)
            else:
                product_qty = line.product_qty
                price_unit = line.price_unit

            if requisition.type_id.quantity_copy != 'copy':
                product_qty = 0

            # Compute price_unit in appropriate currency
            if requisition.company_id.currency_id != currency:
                price_unit = requisition.company_id.currency_id.compute(price_unit, currency)

            # Create PO line
            order_line_values = line._prepare_purchase_order_line(
                name=name, product_qty=product_qty, price_unit=price_unit,
                taxes_ids=taxes_ids)
            order_lines.append((0, 0, order_line_values))
        self.order_line = order_lines
