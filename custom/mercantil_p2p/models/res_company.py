# -*- coding: utf-8 -*-
from odoo import models, fields


class PaymentAcquire(models.Model):
    _inherit = "res.company"

    mercantil_api_key = fields.Char()

    mercantil_secret_key = fields.Char()

    mercantil_client_id = fields.Char()

    mercantil_password_api = fields.Char()
