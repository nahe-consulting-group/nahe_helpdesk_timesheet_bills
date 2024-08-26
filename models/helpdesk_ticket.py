from odoo import models, fields, api
from odoo.exceptions import UserError


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    timesheet_ids = fields.One2many(
        "account.analytic.line", "ticket_id", string="Horas dedicadas"
    )
    total_hours = fields.Float(
        string="Total de horas", compute="_compute_total_hours", store=True
    )

    @api.depends("timesheet_ids.unit_amount")
    def _compute_total_hours(self):
        for ticket in self:
            ticket.total_hours = sum(ticket.timesheet_ids.mapped("unit_amount"))

    def action_invoice_ticket(self):
        self.ensure_one()
        if not self.timesheet_ids:
            raise UserError("No hay horas registradas para facturar.")
        invoice_lines = []
        for line in self.timesheet_ids:
            invoice_lines.append(
                (
                    0,
                    0,
                    {
                        "product_id": line.product_id.id,
                        "quantity": line.unit_amount,
                        "price_unit": line.product_id.lst_price,
                        "name": line.name,
                    },
                )
            )
        invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": invoice_lines,
            }
        )
        return {
            "type": "ir.actions.act_window",
            "name": "Factura",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": invoice.id,
        }
