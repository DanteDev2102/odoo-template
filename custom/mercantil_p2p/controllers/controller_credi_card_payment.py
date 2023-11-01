# -*- coding: utf-8 -*-
from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime

from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo import http, _, fields
from odoo.http import request


class ControllerCrediCardPayment(CustomerPortal):
    @http.route(
        ["/list_payment_acquirers/", "/list_payment_acquirers/<int:page>"],
        auth="public",
        website=True,
        methods=["GET", "POST"],
    )
    def list_payment_acquirers(
        self, page=1, sortby=None, order_id=False, invoice_id=False
    ):
        company = request.env.user.company_ids
        sale_order = False
        invoice = False
        if order_id:
            sale_order = (
                request.env["sale.order"].sudo().search([("id", "=", order_id)])
            )
            company = sale_order.company_id
        if invoice_id:
            invoice = (
                request.env["account.move"].sudo().search([("id", "=", invoice_id)])
            )
            company = invoice.company_id
        if not sortby:
            sortby = "name"
        searchbar_sortings = {
            "name": {"label": _("Name"), "order": "name"},
        }
        sort_order = searchbar_sortings[sortby]["order"]
        domain = [
            ("state", "!=", "disabled"),
            ("provider", "in", ["bdv", "cdcp", "transfer", "bnc", "mercantil"]),
        ]
        if request.env.user.login == "public":
            domain.append(("is_public", "=", True))
        if sale_order or invoice:
            domain.append(("company_id", "=", company.id))
        else:
            domain.append(("company_id", "in", company.ids))
        if sale_order:
            url = f"/list_payment_acquirers/?order_id={order_id}"
        elif invoice:
            url = f"/list_payment_acquirers/?invoice_id={invoice_id}"
        else:
            url = f"/list_payment_acquirers/"
        payment_count = request.env["payment.acquirer"].sudo().search_count(domain)
        pager = portal_pager(
            url=url, total=payment_count, page=page, step=self._items_per_page
        )
        payment_acquirers = (
            request.env["payment.acquirer"]
            .sudo()
            .search(
                domain,
                order=sort_order,
                limit=self._items_per_page,
                offset=pager["offset"],
            )
        )
        request.session["my_documents_history"] = payment_acquirers.ids[:10]
        values = {
            "pager": pager,
            "payment_acquirer_ids": payment_acquirers.sudo(),
            "order_id": order_id,
            "invoice_id": invoice_id,
            "default_url": url,
            "searchbar_sortings": searchbar_sortings,
            "sortby": sortby,
        }
        return request.render("payment_acquirer_list.list_payment_acquirers", values)
