from odoo import api, models, fields, _, SUPERUSER_ID
from odoo.exceptions import UserError
from datetime import datetime


class ConfigElectronicPayment(models.Model):
    _name = "config.electronic.payment"
    _sql_constrains = [
        (
            "config_electronic_payment_unique_company",
            "unique(company_id)",
            _("only one configuration can exist per company"),
        )
    ]

    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company.id
    )

    active = fields.Boolean(default=True)

    invoice_not_fiscal_counter = fields.Integer(default=0)

    invoice_fiscal_counter = fields.Integer(default=0)

    invoice_not_fiscal_interval = fields.Integer(default=0)

    invoice_fiscal_interval = fields.Integer(default=0)

    fiscal_journal = fields.Many2one("account.journal", domain=[("type", "=", "sale")])

    not_fiscal_journal = fields.Many2one(
        "account.journal", domain=[("type", "=", "sale")]
    )

    hour_closed_config = fields.Float()

    def reset_counters_of_day(self):
        cron = self.env["ir.cron"].search(
            [("company_id.name", "=", self.env.company.name)]
        )

        cron.write({"invoice_not_fiscal_counter": 0, "invoice_fiscal_counter": 0})

    def create_cron_reset_counters(self):
        ir_cron = self.env["ir.cron"]

        company_name = self.company_id.name

        cron_data = [
            {
                "name": f"reset counter of day {company_name}",
                "active": True,
                "numbercall": -1,
                "model_id": self.env.ref("base.model_res_company").id,
                "state": "code",
                "user_id": self.env.ref("base.user_root").id,
                "interval_number": 1,
                "interval_type": "days",
                "code": "model.reset_counters_of_day()",
                "doall": False,
            }
        ]

        ir_cron.with_user(SUPERUSER_ID).create(cron_data)

    @api.model
    def create(self, config):
        res = super().create(config)

        for config in self:
            config.create_cron_reset_counters()

        return res

    # TODO: fix determinate minutes
    @api.onchange("hour_closed_config")
    def _onchange_hour_closed_config(self):
        company_name = self.company_id.name

        cron = self.env["ir.cron"].search([("name", "ilike", f"%{company_name}%")])

        current_date = fields.Date.context_today(self)
        hours = int(self.hour_closed_config)

        calculated_minutes = int(60 * (self.hour_closed_config - hours))

        minutes = calculated_minutes % 5 == 0

        if not minutes:
            raise UserError(_("is unique valid numbers multiply 5"))

        config_time = datetime.strptime(
            f"{hours + 4}:{calculated_minutes}:00",
            "%H:%M:%S",
        ).time()

        format_datetime = datetime.combine(current_date, config_time)

        cron.nextcall = format_datetime

    @api.constrains("fiscal_journal")
    def _is_fiscal_journal(self):
        for config in self:
            is_fiscal = config.fiscal_journal.printer_id.is_fiscal

            if not is_fiscal:
                raise UserError(_("only tax journals are accepted"))

    @api.constrains("not_fiscal_journal")
    def _not_fiscal_journal(self):
        for config in self:
            is_fiscal = config.not_fiscal_journal.printer_id.is_fiscal

            if is_fiscal:
                raise UserError(_("only non-tax journals are accepted"))
