# -*- coding: utf-8 -*-
from odoo import models, fields


class PaymentAcquire(models.Model):
    _inherit = "payment.acquirer"

    name = fields.Char()

    provider = fields.Selection(
        selection_add=[("mercantil", "Mercantil")],
        ondelete={"mercantil": "set default"},
    )
