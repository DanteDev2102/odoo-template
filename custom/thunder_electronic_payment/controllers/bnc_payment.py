from odoo import http
from odoo.http import request
from ...bnc_payments.controllers.controllers import ControllerBNCPayment


class BNCPayment(ControllerBNCPayment):
    @http.route(
        ["/bnc/payment"],
        type="http",
        auth="public",
        website=True,
        methods=["GET", "POST"],
    )
    def verify_payment(self, **post):
        res = super().verify_payment(**post)

        order_id = post.get("order_id", False)
        valid_process = request.httprequest.method == "POST" and order_id

        if valid_process:
            order = request.env["sale.order"].browse(int(order_id))

            order.sudo().action_automatic_invoice()

        return res
