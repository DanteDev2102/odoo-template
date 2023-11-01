from odoo import models, fields


class WizardConfigMercantilPayment(models.TransientModel):
    _name = "wizard.config.mercantil.payment"

    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company.id
    )

    mercantil_api_key = fields.Char(
        related="company_id.mercantil_api_key", readonly=False
    )

    mercatil_secret_key = fields.Char(
        related="company_id.mercantil_secret_key", readonly=False
    )

    mercantil_client_id = fields.Char(
        related="company_id.mercantil_client_id", readonly=False
    )

    mercantil_password_api = fields.Char(
        related="company_id.mercantil_password_api", readonly=False
    )
