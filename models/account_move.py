from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    ticket_id = fields.Many2one("helpdesk.ticket", string="Ticket de Soporte")
