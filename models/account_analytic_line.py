from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    ticket_id = fields.Many2one("helpdesk.ticket", string="Ticket de soporte")
    product_id = fields.Many2one("product.product", string="Producto a facturar")
