from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    ticket_id = fields.Many2one("helpdesk.ticket", string="Support ticket")
    product_id = fields.Many2one("product.product", string="Product to Invoice")
    invoiced = fields.Boolean(string="Invoiced", default=False)
