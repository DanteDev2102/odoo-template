from odoo import models
from datetime import datetime
import logging
import pytz

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_automatic_invoice(self):
        company = self.env.company

        for order in self:
            is_transactions = order.transaction_ids

            config = order.env["config.electronic.payment"].search(
                [("company_id", "=", company.id)]
            )

            is_process = not is_transactions or not config or not config.active

            if is_process:
                continue

            is_special_taxpayer = (
                "contribuyente especial"
                in order.partner_id.tax_payer_type_id.name.lower()
            )

            if is_special_taxpayer:
                continue

            order.action_confirm()

            invoice = order._create_invoices()

            hours = int(config.hour_closed_config)

            calculated_minutes = int(60 * (config.hour_closed_config - hours))

            max_time = datetime.strptime(
                f"{hours + 4}:{calculated_minutes}:00",
                "%H:%M:%S",
            ).time()

            ve = pytz.timezone("America/Caracas")
            current_time = datetime.now(tz=ve).time()

            is_valid_time = current_time < max_time

            if not is_valid_time:
                invoice.journal_id = config.not_fiscal_journal.id
                continue

            is_fiscal_client = order.partner_id.vat[0] in ["J", "G"]

            if is_fiscal_client:
                invoice.journal_id = config.fiscal_journal.id
                continue

            possible_create_fiscal_invoice = (
                config.invoice_fiscal_counter < config.invoice_fiscal_interval
            )

            if possible_create_fiscal_invoice:
                invoice.journal_id = config.fiscal_journal.id
                config.invoice_fiscal_counter += 1
                continue

            invoice.journal_id = config.not_fiscal_journal.id

            invoice._post()

            config.invoice_not_fiscal_counter += 1

            reset_counters = (
                config.invoice_not_fiscal_counter == config.invoice_not_fiscal_interval
            )

            if reset_counters:
                config.reset_counters_of_day()
