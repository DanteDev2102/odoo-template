from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = "account.payment"

    is_mercantil_payment = fields.Boolean()
