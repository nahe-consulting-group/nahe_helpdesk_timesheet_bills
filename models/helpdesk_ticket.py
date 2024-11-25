from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date


class HelpdeskTicket(models.Model):
    _inherit = "helpdesk.ticket"

    timesheet_ids = fields.One2many(
        "account.analytic.line", "ticket_id", string="Horas dedicadas"
    )
    total_hours = fields.Float(
        string="Total de horas", compute="_compute_total_hours", store=True
    )
    invoice_ids = fields.Many2many(
        "account.move", string="Facturas", compute="_compute_invoice_ids", store=False
    )

    @api.depends("timesheet_ids")
    def _compute_invoice_ids(self):
        for ticket in self:
            # Buscar las facturas relacionadas con el ticket a través de ticket_id en account.move
            invoices = self.env["account.move"].search([("ticket_id", "=", ticket.id)])
            ticket.invoice_ids = invoices if invoices else False

    @api.depends("timesheet_ids.unit_amount")
    def _compute_total_hours(self):
        for ticket in self:
            ticket.total_hours = sum(ticket.timesheet_ids.mapped("unit_amount"))

    def action_invoice_ticket(self):
        self.ensure_one()

        # Filtrar las líneas que no han sido facturadas
        non_invoiced_lines = self.timesheet_ids.filtered(lambda l: not l.invoiced)

        if not non_invoiced_lines:
            raise UserError("No hay horas sin facturar para este ticket.")

        invoice_lines = []
        for line in non_invoiced_lines:
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
            line.invoiced = True  # Marcar la línea como facturada

        invoice = self.env["account.move"].create(
            {
                "partner_id": self.partner_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": invoice_lines,
                "ticket_id": self.id,  # Guardar el ID del ticket en la factura
                "invoice_date": date.today(),  # Fecha de inicio por defecto
                "l10n_ar_afip_service_start": date.today(),  # Fecha de inicio por defecto
                "l10n_ar_afip_service_end": date.today(),  # Fecha de fin por defecto
            }
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Factura",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": invoice.id,
        }
